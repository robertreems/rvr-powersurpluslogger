resource "azurerm_resource_group" "rvrlogging" {
  name     = "rvrlogging"
  location = "westeurope"
  tags     = { LifeCycle = "test" }
}

module "log_analytics_workspace" {
    source = "./modules/log_analytics_workspace"
    location = azurerm_resource_group.rvrlogging.location
    name = "MyfirstLogAnalytics"
    resource_group_name = azurerm_resource_group.rvrlogging.name
}

module "service_principal"{
    source = "./modules/service_principal"
}

