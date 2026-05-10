from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr, SecretStr
from typing import Optional, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class User(BaseModel):
    age: int | None = None
    name: str = "Gleb"
    email: str = "glebsmailbox@gmail.com"


user = User()
print(user)
user_dict = user.model_dump_json()
data = {"name": "Gleb", "age": "18", "email": "glebsmailbox@gmail.com"}
user = User(**data)
user = User.model_validate(data)
print(user)


# ----------------


class APIConfig(BaseModel):
    api_key: str
    model: str = "gpt-4"
    max_tokens: int = 1000
    temperature: float = 0.7


config = APIConfig(api_key="4", temperature=3)
config.temperature


# ---------------


class Client(BaseModel):
    name: str
    email: str


def greet_user(user: User) -> str:
    return f"Hello, {user.name}!"


def load_user(data: dict) -> User:
    return User.model_validate(data)


# ---------------


class WeatherResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    city: str
    temperature: float
    humidity: int
    description: str


api_data = {
    "city": "Klagenfurt",
    "temperature": 20,
    "humidity": 60,
    "description": "Partly cloudy",
}
weather = WeatherResponse.model_validate(api_data)
print(
    weather.city,
    "\n",
    weather.temperature,
    "\n",
    weather.humidity,
    "\n",
    weather.description,
)


class User(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(default=18, gt=0, le=120)
    email: str


user = User(name="Gleb", age=18, email="glebs")


# ---------


class ClientModel(BaseModel):
    username: str
    email: EmailStr

    @field_validator("username")
    def validate_username(cls, v):
        if " " in v:
            raise ValueError("Username cannot contain spaces")
        return v.lower()


user = ClientModel(username="GlebMat", email="glebsmailbox@gmail.com")
print(user.username)


class OrderItem(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(ge=0)
    adress: str = Field(min_length=4)
    quantity: int = Field(gt=0)


class Order(BaseModel):
    recipient_id: int = Field(ge=0)
    items: list[OrderItem]


order = Order(
    recipient_id=320972,
    items=[
        OrderItem(
            name="Die Eier aus Bodenhaltung",
            price=3.49,
            adress="Bahnhofstrasse 20, 9020 Klagenfurt-am-Woerthersee",
            quantity=3,
        )
    ],
)
order.model_dump()
order.model_json_schema()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    api_key: SecretStr


settings = Settings()
print(settings.model_dump())


# -------------


class ProductInfo(BaseModel):
    name: str
    price: float
    category: str
    in_stock: bool
    is_worth_buying: bool = Field(
        description="Explain whether you think the item is worth buying at the given price or not."
    )


client = OpenAI()

response = client.responses.parse(
    model="gpt-4o",
    input="Extract:The new MacBook Pro costs $1999 and is available in Electronics now.",
    text_format=ProductInfo,
)
response.output_parsed
product = response.output_parsed

print(product.name)
print(product.price)
print(product.category)
print(product.in_stock)
print(product.is_worth_buying)


# -------


class SentimentalAnalysis(BaseModel):
    text: str
    sentimental: Literal["positive", "negative", "neutral"]
    confidence: float


class Classification(BaseModel):
    text: str
    category: Literal["bug", "feature", "question", "other"]
    priority: Literal["low", "medium", "high"]


# ---------
class LineItem(BaseModel):
    description: str
    quantity: int = Field(ge=1)
    unit_price: float = Field(ge=0)

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price


class Invoice(BaseModel):
    invoice_number: str
    date: str
    vendor_name: str
    vendor_address: str | None = None
    items: list[LineItem]
    subtotal: float
    tax: float | None = None
    total: float
    payment_status: Literal["paid", "pending", "overdue"] = "pending"


# Extract from invoice text
invoice_text = """
Invoice #INV-2025-001
Date: January 15, 2025
From: Acme Corp, 123 Business St

Items:
- Widget Pro (5) @ $29.99 each
- Service Fee (1) @ $50.00

Subtotal: $199.95
Tax: $16.00
Total: $215.95

They have recently paid for that.
"""

client = OpenAI()
response = client.responses.parse(
    model="gpt-4o", input=f"Extract invoice data:\n{invoice_text}", text_format=Invoice
)

invoice = response.output_parsed
print(f"Invoice: {invoice.invoice_number}")
print(f"From: {invoice.vendor_name}")
print(f"Total: ${invoice.total}")
print(f"Status: {invoice.payment_status}")
