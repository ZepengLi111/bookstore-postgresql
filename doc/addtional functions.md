# 后40%内容的接口文档

## 发货

#### URL:

POST http://[address]/seller/send

#### Request

##### Header:

| key   | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | N          |

##### Body:

```json
{
    "user_id": "seller_id",
    "order_id": "order_id",
    "store_id": "store_id"
}
```

##### 属性说明：

| 变量名   | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| user_id  | string | 卖家用户ID | N          |
| order_id | string | 订单ID     | N          |
| store_id | string | 商店ID     | N          |

#### Response

Status Code:

| 码   | 描述                 |
| ---- | -------------------- |
| 200  | 发货成功             |
| 511  | 卖家用户ID不存       |
| 513  | 商店ID不存在         |
| 518  | 订单ID不存在         |
| 523  | 订单状态错误         |
| 524  | 商店ID和卖家ID不匹配 |

Body:

```
{
    "message":"$error message$"
}
```

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------- |
| message | string | 返回错误消息，成功时为"ok" | N          |

## 收货

#### URL:

POST http://[address]/buyer/receive

#### Request

##### Header:

| key   | 类型   | 描述               | 是否可为空 |
| ----- | ------ | ------------------ | ---------- |
| token | string | 登录产生的会话标识 | N          |

##### Body:

```json
{
    "user_id": "buyer_id",
    "order_id": "order_id",
}
```

##### 属性说明：

| 变量名   | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| user_id  | string | 买家用户ID | N          |
| order_id | string | 订单ID     | N          |

#### Response

Status Code:

| 码   | 描述             |
| ---- | ---------------- |
| 200  | 收货成功         |
| 511  | 买家用户ID不存在 |
| 5X3  | 订单ID不存在     |
| 523  | 订单状态错误     |

Body:

```
{
    "message":"$error message$"
}
```

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------- |
| message | string | 返回错误消息，成功时为"ok" | N          |

## 订单查询

#### URL

POST http://[address]/buyer/check_order

#### Request

##### Body:

```json
{
  "user_id": "user_id",
  "order_id": "order_id",
}
```

##### 属性说明：

| key      | 类型   | 描述             | 是否可为空 |
| -------- | ------ | ---------------- | ---------- |
| user_id  | string | 查询用户历史订单 | N          |
| order_id | string | 查询的订单ID     | N          |

#### Response

Status Code:

| 码   | 描述           |
| ---- | -------------- |
| 200  | 查询成功       |
| 401  | 查询失败       |
| 522  | 无效参数       |
| 513  | user_id不存在  |
|      | order_id不存在 |

Body:

```
{
    "message":"$error message$"，
    "data": "",
}
```

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------- |
| message | string | 返回错误消息，成功时为"ok" | N          |
| data    | json   | 返回订单的的详细信息       | N          |

## 取消订单

#### URL

POST http://[address]/buyer/cancel_order


#### Request

##### Body:

```json
{
  "user_id": "user_id",
  "order_id": "order_id"
}
```

##### 属性说明：

| key      | 类型   | 描述             | 是否可为空 |
| -------- | ------ | ---------------- | ---------- |
| user_id  | string | 用户id           | N          |
| order_id | string | 想要取消的订单id | N          |

#### Response

Status Code:

| 码   | 描述           |
| ---- | -------------- |
| 200  | 取消成功       |
| 401  | 取消失败       |
| 522  | 无效参数       |
| 513  | user_id不存在  |
| 518  | order_id不存在 |
|      |                |

Body:

```
{
    "message":"$error message$"，
}
```

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------- |
| message | string | 返回错误消息，成功时为"ok" | N          |

## 全局搜索

#### URL：

POST http://[address]/buyer/search_global

#### Request

##### Body:

```json
{
  "keyword": "keyword",
  "page": "page",
  "user_id": "user_id" 
}
```

##### 属性说明：

| key     | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------- |
| keyword | string | 搜索关键词                 | N          |
| page    | int    | 页数，0代表不分页，默认为0 | Y          |
| user_id | string | 用户ID                     | N          |

#### Response

Status Code:

| 码   | 描述     |
| ---- | -------- |
| 200  | 搜索成功 |
| 401  | 搜索失败 |
| 522  | 无效参数 |

Body:

```
{
    "message":"$error message$"，
    "books": "",
    "count": "",
}
```

| 变量名  | 类型    | 描述                                   | 是否可为空 |
| ------- | ------- | -------------------------------------- | ---------- |
| message | string  | 返回错误消息，成功时为"ok"             | N          |
| books   | list    | 成功时返回搜索到的图书id，失败时返回空 | Y          |
| count   | integer | 搜索到的总结果数量                     | N          |
| page    | int     | 第几页                                 | N          |

## 店铺搜索

#### URL：

POST http://[address]/buyer/search_in_store

#### Request

##### Body:

```json
{
  "keyword": "keyword",
  "page": "page",
  "store_id": "store_id",
  "user_id": "user_id"
}
```

##### 属性说明：

| key      | 类型   | 描述                       | 是否可为空 |
| -------- | ------ | -------------------------- | ---------- |
| keyword  | string | 搜索关键词                 | N          |
| page     | int    | 页数，0代表不分页，默认为0 | Y          |
| store_id | string | 商铺ID                     | N          |
| user_id  | string | 用户ID                     | N          |

#### Response

Status Code:

| 码   | 描述       |
| ---- | ---------- |
| 200  | 搜索成功   |
| 401  | 搜索失败   |
| 522  | 无效参数   |
| 513  | 店铺不存在 |

Body:

```
{
    "message":"$error message$"，
    "books": ""
}
```

| 变量名  | 类型    | 描述                                   | 是否可为空 |
| ------- | ------- | -------------------------------------- | ---------- |
| message | string  | 返回错误消息，成功时为"ok"             | N          |
| books   | json    | 成功时返回搜索到的图书id，失败时返回空 | Y          |
| count   | integer | 搜索到的结果数量                       | N          |
| page    | int     | 第几页                                 | N          |