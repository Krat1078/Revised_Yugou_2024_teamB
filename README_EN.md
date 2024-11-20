

# Project Directory Structure

```plaintext
Revised_Yugou_2024_teamB/
│
├── LostItemproject/
│   ├── LostItemproject/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │
│   ├── top/
│   │   ├──media/
│   │   │   ├──images/
│   │   │
│   │   ├── migrations/
│   │   │   ├── 0001_initial.py
│   │   │   ├── __init__.py
│   │   │
│   │   ├── templates/
│   │   │   ├──index.html
│   │   │
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
│   │
│   ├── db.sqlite3
│   ├── manage.py
│
├── assets/
│   ├── images/
│   │   ├── DatabaseStructure.png
│   │
│   ├── SharedFolders/
│       ├── initSQL.mwb
│       ├── initSQL2.mwb
│       ├── initSQL3_kurosaka.mwb
│       ├── initSQL4.mwb
│       ├── lostitems.sql
│
├── README.md
├── README_EN.md
```


# Database Structure Documentation for the LostItemProject

![DatabaseStructure.png](/assets/images/DatabaseStructure.png)

## Overview

This documentation describes the database schema for a campus lost-and-found management platform, implemented using Django. The database is designed to store and manage information about lost and found items, including their categories, locations, storage, images, and status.

---

## Application and Models

The database schema corresponds to Django models within the `top` application. Below is an explanation of each model and its structure.

---

## Models

### 1. **`ItemNameTag`**

This model stores categories or tags for items (e.g., stationery, clothing, electronic equipment).

| Field Name | Data Type | Description |
| --- | --- | --- |
| `id` | AutoField (Primary Key) | Unique identifier for each item category. |
| `name` | CharField (max_length=100) | Name of the category (e.g., "Stationery"). |
| `description` | TextField (optional) | Additional details about the category. |

---

### 2. **`PickedOrDroppedLocationTag`**

This model records the locations where items were found or lost.

| Field Name | Data Type | Description |
| --- | --- | --- |
| `id` | AutoField (Primary Key) | Unique identifier for each location tag. |
| `name` | CharField (max_length=100) | Name of the location (e.g., "Student Center"). |
| `description` | TextField (optional) | Additional details about the location. |

---

### 3. **`StorageLocationTag`**

This model manages locations where lost items are stored temporarily.

| Field Name | Data Type | Description |
| --- | --- | --- |
| `id` | AutoField (Primary Key) | Unique identifier for each storage location. |
| `name` | CharField (max_length=100) | Name of the storage location (e.g., "Library"). |
| `description` | TextField (optional) | Additional details about the storage location. |

---

### 4. **`Item`**

This model stores information about individual items, including their category, discovery location, storage location, and contact details.

| Field Name | Data Type | Description |
| --- | --- | --- |
| `id` | AutoField (Primary Key) | Unique identifier for each item. |
| `item_name` | ForeignKey (to `ItemNameTag`) | Item category, referencing `ItemNameTag`. |
| `picked_or_dropped_location` | ForeignKey (to `PickedOrDroppedLocationTag`) | Location where the item was found or lost. |
| `storage_location` | ForeignKey (to `StorageLocationTag`) | Storage location for the item. |
| `item_type` | IntegerField | Indicates if the item is lost or found (`0: Found`, `1: Lost`). |
| `status` | SmallIntegerField | Processing status (`0: Pending`, `1: In Progress`, `2: Resolved`). |
| `created_at` | DateTimeField | Timestamp when the item record was created. |
| `updated_at` | DateTimeField (optional) | Timestamp when the item record was last updated. |
| `contact_email` | CharField (max_length=100, optional) | Contact email for the item. |
| `contact_phone` | CharField (max_length=20, optional) | Contact phone number for the item. |

---

### 5. **`ItemImage`**

This model stores images related to items.

| Field Name | Data Type | Description |
| --- | --- | --- |
| `id` | AutoField (Primary Key) | Unique identifier for each image. |
| `item` | ForeignKey (to `Item`) | References the item associated with the image. |
| `image_path` | CharField (max_length=225) | File path of the image. |
| `uploaded_at` | DateTimeField (optional) | Timestamp when the image was uploaded. |

---

## Relationships

- **`ItemNameTag` ↔ `Item`**: Each item belongs to a specific category.
- **`PickedOrDroppedLocationTag` ↔ `Item`**: Each item has a location where it was found or lost.
- **`StorageLocationTag` ↔ `Item`**: Each item has a storage location.
- **`Item` ↔ `ItemImage`**: Each item can have multiple associated images.

---

## Example Use Cases

1. **Adding a Lost Item**: Record the item's category, discovery location, storage location, and contact details.
2. **Uploading Images**: Attach one or more images to an item for easier identification.
3. **Tracking Item Status**: Update the status field to track the item's progress (e.g., resolved).
4. **Category and Location Management**: Dynamically add or update item categories and location tags.

---

## Advantages of the Design

- **Normalized Structure**: Separate tables for categories, locations, and items ensure minimal redundancy and easier management.
- **Flexible Extensions**: Allows dynamic addition of new categories and locations without altering the core item table.
- **Multi-Image Support**: Facilitates the attachment of multiple images per item.
- **Status Tracking**: Enables efficient workflow management for lost-and-found operations.