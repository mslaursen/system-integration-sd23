# Generate random resource group name
resource "random_pet" "rg_name" {
  prefix = var.resource_group_name_prefix
}

resource "azurerm_resource_group" "rg" {
  location = var.resource_group_location
  name     = random_pet.rg_name.id
}

# Generate random value for the name
resource "random_string" "name" {
  length  = 8
  lower   = true
  numeric = false
  special = false
  upper   = false
}


# Manages the MySQL Flexible Server
resource "azurerm_mysql_flexible_server" "default" {
  location                     = azurerm_resource_group.rg.location
  name                         = "mysqlfs-${random_string.name.result}"
  resource_group_name          = azurerm_resource_group.rg.name
  administrator_login          = random_string.name.result
  administrator_password       = "P4ssword!"
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  sku_name                     = "GP_Standard_D2ds_v4"
  version                      = "8.0.21"
}


resource "azurerm_mysql_firewall_rule" "example" {
  name                = "office"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_mysql_flexible_server.default.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
}
