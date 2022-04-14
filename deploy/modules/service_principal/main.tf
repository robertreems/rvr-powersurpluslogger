data "azuread_client_config" "current" {}

resource "azuread_application" "application" {
  display_name = "rvr_application"
  owners       = [data.azuread_client_config.current.object_id]
}

resource "azuread_service_principal" "example" {
  application_id               = azuread_application.application.application_id
  app_role_assignment_required = false
  owners                       = [data.azuread_client_config.current.object_id]
}

resource "azuread_service_principal_password" "myfirstprincipalpassword" {
  service_principal_id = azuread_service_principal.example.object_id
}
