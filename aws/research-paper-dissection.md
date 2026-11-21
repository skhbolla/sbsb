# DynamoDB

## Features

- MultiTenant - Load of one customer should not effect other customers
- High resource utilization - ??
- Boundless scale of tables - No limit on how big tables can be.
- Predictable performance - irrespecitve of data scale
- Highly available - Replication across AZs ,and recovery
- Schemaless - Supports larger usecase possibilities

## Architecture

- DynamoDB tables are a `collection of items`
- Each item is identified by a `primary key`
- `primary key` = `partition key + sort key` (Note: Sort key is optional)


## How Keys Determine Storage

- Partition Key Routing: DynamoDB passes only the partition key value into an internal hash function. The resulting hash output dictates which physical storage partition holds the item.
- Sort Key Ordering: Once the partition is selected, DynamoDB groups all items sharing that partition key together into an item collection. The sort key is then used strictly to sort those items in ascending order within that partition

## Secondary Indexes

Secondary indexes are just tables with just two columns.
They map the `indexed value` to the `primary key`
