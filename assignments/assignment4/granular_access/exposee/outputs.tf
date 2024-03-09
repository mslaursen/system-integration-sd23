output "azurerm_mysql_flexible_server" {
  value = azurerm_mysql_flexible_server.default.name
}

output "admin_login" {
  value = azurerm_mysql_flexible_server.default.administrator_login
}

output "mysql_flexible_server_database_name" {
  value = azurerm_mysql_flexible_database.main.name
}

output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}
