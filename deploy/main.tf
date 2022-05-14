resource "azurerm_resource_group" "rvrlogging" {
  name     = "rvrlogging"
  location = "westeurope"
  tags     = { LifeCycle = "test" }
}

# Used by the script rvrpowerlogger.
module "log_analytics_workspace" {
    source = "./modules/log_analytics_workspace"
    location = azurerm_resource_group.rvrlogging.location
    name = "MyfirstLogAnalytics"
    resource_group_name = azurerm_resource_group.rvrlogging.name
}

# Used by the script rvrstatisticslogger.
module "log_analytics_workspace_powerstatistics" {
    source = "./modules/log_analytics_workspace"
    location = azurerm_resource_group.rvrlogging.location
    name = "powerstatistics"
    resource_group_name = azurerm_resource_group.rvrlogging.name
    retention_in_days = 730
}

module "service_principal"{
    source = "./modules/service_principal"
}

