# listany

## Models

### Link
Field | Type | Description
---|---|---
id | uuid |
url | string | The URL of the link
title | string | The title of the link
description | string | The description of the link
created_at | datetime | The date the link was created
updated_at | datetime | The date the link was updated
created_by | uuid | The user who created the link

### Collection
Field | Type | Description
---|---|---
id | uuid |
name | string | The name of the collection
description | string | The description of the collection
created_at | datetime | The date the collection was created
updated_at | datetime | The date the collection was updated
created_by | uuid | The user who created the collection
links | foreign key | The links in the collection


### Tags
Field | Type | Description
---|---|---
id | uuid |
name | string | The name of the tag
description | string | The description of the tag
created_at | datetime | The date the tag was created
updated_at | datetime | The date the tag was updated
created_by | uuid | The user who created the tag
links | foreign key | The links with the tag
collections | foreign key | The collections with the tag
