terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>2.46.0"
    }
  }
}

resource "azurerm_mysql_server" "mysql" {
  name                = "granular-access-mysql"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  sku_name   = "GP_Gen5_2"
  storage_mb = 5120
  version    = "5.7"

  administrator_login          = "granular-access"
  administrator_login_password = "P4ssword1234!"

  auto_grow_enabled                 = true
  backup_retention_days             = 7
  geo_redundant_backup_enabled      = true
  infrastructure_encryption_enabled = true
  public_network_access_enabled     = true
  ssl_enforcement_enabled           = true
  ssl_minimal_tls_version_enforced  = "TLS1_2"
}


resource "azurerm_mysql_database" "mysql" {
  name                = "granular-access-db"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_mysql_server.mysql.name
  charset             = "UTF8"
  collation           = "UTF8_GENERAL_CI"
}
