# Manages the MySQL Flexible Server Database
resource "azurerm_mysql_flexible_database" "main" {
  charset             = "utf8mb4"
  collation           = "utf8mb4_unicode_ci"
  name                = "store-db"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_mysql_flexible_server.default.name
}

resource "null_resource" "db_init" {
  depends_on = [azurerm_mysql_flexible_database.main]

  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = "mysql -h ${azurerm_mysql_flexible_server.default.fqdn} -u ${azurerm_mysql_flexible_server.default.administrator_login} --password=P4ssword! ${azurerm_mysql_flexible_database.main.name} < ./init.sql"
  }
}
