
# Database Integration Guide for Integrator User

This document serves as a guide for connecting to the database as the `integrator` user and outlines the user's permissions regarding various database operations.

## Prerequisuites

MySQL is installed on your machine

## Connecting to the Database

To connect to the database as the `integrator` user, use the following credentials:

- **Username:** integrator
- **Password:** verysecret
- **Host:** granular-access-mysql.mysql.database.azure.com 

You can connect to the database using a database client or a command-line tool. For example, using the MySQL command-line tool, you would enter the following command:

```bash
mysql -u integrator -p -h granular-access-mysql.mysql.database.azure.com
```

After executing the command, you will be prompted to enter the password. Provide the `integrator` user's password when prompted.

## Database Tables Overview

The database contains the following tables:

1. **users** - Stores user information including their roles.
2. **products** - Contains details about products.
3. **orders** - Tracks user orders.
4. **order_products** - Links orders with the products ordered, including quantities.

## Integrator User Permissions

The `integrator` user is granted specific permissions to ensure data integrity while allowing for necessary operations on the database. Below are the permissions detailed by table:

### users Table

- **SELECT** on `id`, `email`, and `role` columns: The `integrator` user can view the ID, email, and role of users, which is essential for associating orders and managing access based on roles.

### products Table

- **SELECT** on all columns: Allows viewing all details of products.
- **UPDATE** on `description` and `stock_quantity`: The `integrator` can update the product descriptions and the stock quantities, facilitating inventory management.

### orders Table

- **SELECT**, **INSERT**, **UPDATE**: Enables the `integrator` to view all order details, add new orders, and update existing orders, such as changing order statuses.

### order_products Table

- **SELECT**, **INSERT**, **UPDATE**: Allows the `integrator` to manage the products within orders, including adding new products to orders and updating quantities.

## Example Operations

### Viewing Products

To view details of all products:

```sql
SELECT * FROM products;
```

### Updating Product Stock

To update the stock quantity of a product:

```sql
UPDATE products SET stock_quantity = [new_quantity] WHERE id = [product_id];
```

Replace `[new_quantity]` with the new stock quantity and `[product_id]` with the ID of the product you wish to update.

