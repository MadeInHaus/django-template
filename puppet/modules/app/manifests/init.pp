class app {
    class{'app::apt-get-update': stage => first }
    class{'app::configuration-actions': stage => last }
}
