terraform {
  required_providers {
    azurerm = {
      version = "~> 3"
    }
  }
}

provider "azurerm" {
  features {}
}
