from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import admin

from django.conf import settings

def admin_url(model, url, object_id=None):
    """
    Returns the URL for the given model and admin url name.
    """
    opts = model._meta
    url = "admin:%s_%s_%s" % (opts.app_label, opts.object_name.lower(), url)
    args = ()
    if object_id is not None:
        args = (object_id,)
    return reverse(url, args=args)


class SingletonAdmin(admin.ModelAdmin):
    """
    Admin class for models that should only contain a single instance
    in the database. Redirect all views to the change view when the
    instance exists, and to the add view when it doesn't.
    
    *** NOTE:be sure to copy the change_form.html into your templates/admin/ directory and add
    a data-singleton attribute to the div containing the submit row like so:
            <div data-singleton="{% if singleton %}true{% else %}false{% endif %}">
    and add singleton.js to your static/admin/js directory.
    
    Works with grappelli,  may need to be modified for other admin frameworks.
    """

    def handle_save(self, request, response):
        """
        Handles redirect back to the dashboard when save is clicked
        (eg not save and continue editing), by checking for a redirect
        response, which only occurs if the form is valid.
        """
        form_valid = isinstance(response, HttpResponseRedirect)
        if request.POST.get("_save") and form_valid:
            return redirect("admin:index")
        return response

    def add_view(self, *args, **kwargs):
        """
        Redirect to the change view if the singleton instance exists.
        """
        try:
            singleton = self.model.objects.get()
        except (self.model.DoesNotExist, self.model.MultipleObjectsReturned):
            kwargs.setdefault("extra_context", {})
            kwargs["extra_context"]["singleton"] = True
            response = super(SingletonAdmin, self).add_view(*args, **kwargs)
            return self.handle_save(args[0], response)
        return redirect(admin_url(self.model, "change", singleton.id))

    def changelist_view(self, *args, **kwargs):
        """
        Redirect to the add view if no records exist or the change
        view if the singleton instance exists.
        """
        try:
            singleton = self.model.objects.get()
        except self.model.MultipleObjectsReturned:
            singleton = self.models.objects.all()[0]
        except self.model.DoesNotExist:
            return redirect(admin_url(self.model, "add"))
        return redirect(admin_url(self.model, "change", singleton.id))

    def change_view(self, *args, **kwargs):
        """
        If only the singleton instance exists, pass ``True`` for
        ``singleton`` into the template which will use js to hide
        the "save and add another" button.
        """
        kwargs.setdefault("extra_context", {})
        kwargs["extra_context"]["singleton"] = self.model.objects.count() == 1
        
        response = super(SingletonAdmin, self).change_view(*args, **kwargs)
        return self.handle_save(args[0], response)
    
    class Media:
        js = [
              settings.STATIC_URL+'admin/js/singleton.js',
              ]


class SortableInlineAdmin(admin.TabularInline):
    extra = 0
    sortable_field_name = "position"

    class Meta:
        ordering = ['position']

    class Media:
        css = {'all': (settings.STATIC_URL+'admin/css/custom_admin.css', )}


class SortableStackedInlineAdmin(admin.StackedInline):
    extra = 0
    sortable_field_name = "position"

    class Meta:
        ordering = ['position']

    class Media:
        css = {'all': (settings.STATIC_URL+'admin/css/custom_admin.css', )}
        