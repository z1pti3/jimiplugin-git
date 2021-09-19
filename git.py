from core import plugin, model


class _git(plugin._plugin):
    version = 0.7

    def install(self):
        # Register  Models
        model.registerModel(
            "GitOps",
            "_GitOps",
            "_action",
            "plugins.git.models.action",
        )
        model.registerModel(
            "GitClone",
            "_GitClone",
            "_action",
            "plugins.git.models.action",
        )
        return True

    def uninstall(self):
        # de-register  Models
        model.deregisterModel(
            "GitOps",
            "_GitOps",
            "_action",
            "plugins.git.models.action",
        )
        model.deregisterModel(
            "GitClone",
            "_GitClone",
            "_action",
            "plugins.git.models.action",
        )
        return True

    def upgrade(self, LatestPluginVersion):

        if self.version < 0.1:
            model.registerModel(
                "GitOps",
                "_GitOps",
                "_action",
                "plugins.git.models.action",
            )
        if self.version < 0.2:
            model.registerModel(
                "GitClone",
                "_GitClone",
                "_action",
                "plugins.git.models.action",
            )
        return True
