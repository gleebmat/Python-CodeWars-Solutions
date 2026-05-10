import os
from openai import OpenAI
from pydantic import BaseModel, Field
from datetime import datetime
import logging
from typing import Optional


logging.basicConfig(
    level=logging.INFO,  # we need only log messages with status INFO and above
    format="%(asctime)s - %(levelname)s - %(message)s",  # this defines the format of the log output
    datefmt="%Y-%m-%d %H:%M:%S",  # this defines to a human-readable format the timestamp in the logs
)

logger = logging.getLogger(
    __name__
)  # this particular logger will be used for this module

client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
model = "gpt-4o"


class EventExtraction(BaseModel):
    """We are extracting the initial info about the potential event"""

    description: str = Field(description="Description of the event")
    is_calendar_event: bool = Field(
        description="Whether this text describes a calendar event or not"
    )
    confidence_score: float = Field(
        description="A score from 0 to 1 as your confidence that this text is a calendar event description"
    )


class EventDetails(BaseModel):
    """We are extracting the details of the actual event"""

    name: str = Field(description="The name of the event")
    date: str = Field(description="The date of the event in the ISO 8601 format")
    participants: list[str] = Field(description="The list of participants in the event")


class EventConfirmation(BaseModel):
    """We are confirming the details of the event with the user (with a message)"""

    confirmation_message: str = Field(
        description="Natural language confirmation message"
    )
    calendar_link: Optional[str] = Field(
        description="Generated calendar link if applicable"
    )


def extract_event_info(user_input: str) -> EventExtraction:
    logger.info("Starting event extraction analysis")
    logger.debug(f"Input text: {user_input}")

    today = datetime.now()
    date_context = f"Today is {today.strftime('%A, %B %d, %Y')}."
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"{date_context}. Analyze if the text describes an appropriate calendar event.",
            },
            {"role": "user", "content": user_input},
        ],
        response_format=EventExtraction,
    )
    result = completion.choices[0].message.parsed
    logger.info(
        f"Completed event extraction analysis\nIs Calendar Event:{result.is_calendar_event}\nConfidence Score: {result.confidence_score}"
    )
    return result


def parse_event_details(description: str) -> EventDetails:
    logger.info("Starting event details parsing")

    today = datetime.now()
    date_context = f"Today is {today.strftime('%A, %B %d, %Y')}."

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"{date_context}. Extract the event details from the following description: {description}",
            },
        ],
        response_format=EventDetails,
    )
    result = completion.choices[0].message.parsed
    logger.info(
        f"Event details:\nName: {result.name}\nDate: {result.date}\nParticipants: {', '.join(result.participants)}"
    )
    return result


def generate_confirmation(event_details: EventDetails) -> EventConfirmation:
    logger.info("Generating confirmation message")

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"Generate a confirmation message for the following event details:\nName: {event_details.name}\nDate: {event_details.date}\nParticipants: {', '.join(event_details.participants)}",
            },
            {"role": "user", "content": str(event_details.model_dump())},
        ],
        response_format=EventConfirmation,
    )
    result = completion.choices[0].message.parsed
    logger.info("Generated confirmation message successully!")
    return result


def process_calendar_request(user_input: str) -> Optional[EventConfirmation]:
    logger.info("Processing calendar request")
    logger.debug(f"User input:{user_input}")

    initial_extraction = extract_event_info(user_input)

    if (
        not initial_extraction.is_calendar_event
        or initial_extraction.confidence_score < 0.7
    ):
        logger.warning(
            f"Gate check failed :(\n Is Calendar Event: {initial_extraction.is_calendar_event}\nConfidence Score: {initial_extraction.confidence_score}"
        )
        return None

    logger.info("Gate check passed! Going on...")

    event_details = parse_event_details(initial_extraction.description)

    confirmation = generate_confirmation(event_details)

    logger.info("Completed processing calendar request")

    return confirmation


user_input = input()

result = process_calendar_request(user_input)
if result:
    print(f"Confirmation: {result.confirmation_message}")
    if result.calendar_link:
        print(f"Calendar Link: {result.calendar_link}")
else:
    print("This does not seem a calendar event or I am not confident enough about it.")
