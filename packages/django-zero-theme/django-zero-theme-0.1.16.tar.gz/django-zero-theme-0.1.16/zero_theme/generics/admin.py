from import_export.admin import ImportExportModelAdmin


class ZeroAdmin(ImportExportModelAdmin):
    """Will be assigned dynamically from Admin class"""
    def get_resource_class(self):
        resource = super().get_resource_class()
        resource.Meta.model = self.model
        return resource
