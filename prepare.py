"""
Generate synthetic clinical notes with exact character-level ground truth spans.

Usage:
    uv run prepare.py --count 500
"""

import argparse
import json
import os
import random
import re
from collections import Counter
from pathlib import Path

from faker import Faker

from templates import TEMPLATES

fake = Faker()

PLACEHOLDER_TO_LABEL = {
    "patient_name": "patient_name",
    "patient_first": "patient_name",
    "patient_last": "patient_name",
    "provider_name": "provider_name",
    "provider_first": "provider_name",
    "provider_last": "provider_name",
    "dob": "date",
    "admission_date": "date",
    "discharge_date": "date",
    "appointment_date": "date",
    "procedure_date": "date",
    "phone": "phone_number",
    "fax": "phone_number",
    "email": "email",
    "ssn": "ssn",
    "mrn": "mrn",
    "street_address": "address",
    "city": "address",
    "state": "address",
    "zip_code": "address",
    "full_address": "address",
    "health_plan_number": "health_plan_number",
    "account_number": "account_number",
    "license_number": "license_number",
    "dea_number": "license_number",
    "device_id": "device_id",
    "url": "url",
    "ip_address": "ip_address",
}

PLACEHOLDER_RE = re.compile(r"\{(\w+)\}")


def generate_phi() -> dict[str, str]:
    first = fake.first_name()
    last = fake.last_name()
    prov_first = fake.first_name()
    prov_last = fake.last_name()
    street = fake.street_address()
    city = fake.city()
    state = fake.state_abbr()
    zipcode = fake.zipcode()

    return {
        "patient_name": f"{first} {last}",
        "patient_first": first,
        "patient_last": last,
        "provider_name": f"{prov_first} {prov_last}",
        "provider_first": prov_first,
        "provider_last": prov_last,
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=95).strftime("%m/%d/%Y"),
        "admission_date": fake.date_this_year().strftime("%m/%d/%Y"),
        "discharge_date": fake.date_this_year().strftime("%m/%d/%Y"),
        "appointment_date": fake.date_this_year().strftime("%m/%d/%Y"),
        "procedure_date": fake.date_this_year().strftime("%m/%d/%Y"),
        "phone": fake.phone_number(),
        "fax": fake.phone_number(),
        "email": fake.email(),
        "ssn": fake.ssn(),
        "mrn": f"MRN-{fake.numerify('######')}",
        "street_address": street,
        "city": city,
        "state": state,
        "zip_code": zipcode,
        "full_address": f"{street}, {city}, {state} {zipcode}",
        "health_plan_number": fake.bothify("??#########"),
        "account_number": fake.numerify("ACCT-########"),
        "license_number": fake.bothify("??######"),
        "dea_number": fake.bothify("??#######"),
        "device_id": fake.bothify("SN-????-########"),
        "url": fake.url(),
        "ip_address": fake.ipv4(),
    }


def render_note(
    template_text: str, phi: dict[str, str]
) -> tuple[str, list[dict]]:
    """Render a template with PHI values, tracking exact character spans.

    Builds the output string piece-by-piece from left to right, recording
    the position of each substituted value as we go. This avoids any
    search-based span recovery and is correct even when the same PHI value
    appears multiple times or in the literal text.
    """
    # Find all placeholder matches sorted by position
    matches = list(PLACEHOLDER_RE.finditer(template_text))

    entities: list[dict] = []
    parts: list[str] = []
    output_pos = 0
    prev_end = 0  # end of previous match in template

    for m in matches:
        placeholder = m.group(1)
        if placeholder not in phi:
            # Not a PHI placeholder — leave it as literal text
            continue

        # Append literal text between previous match end and this match start
        literal = template_text[prev_end : m.start()]
        parts.append(literal)
        output_pos += len(literal)

        # Append the PHI value and record the span
        value = phi[placeholder]
        start = output_pos
        parts.append(value)
        output_pos += len(value)

        label = PLACEHOLDER_TO_LABEL[placeholder]
        entities.append(
            {"text": value, "label": label, "start": start, "end": output_pos}
        )

        prev_end = m.end()

    # Append any remaining literal text after the last placeholder
    tail = template_text[prev_end:]
    parts.append(tail)

    rendered = "".join(parts)
    return rendered, entities


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate synthetic clinical notes with ground truth spans."
    )
    parser.add_argument(
        "--count", type=int, default=500, help="Number of notes to generate"
    )
    args = parser.parse_args()

    Faker.seed(42)
    random.seed(42)

    fixtures_dir = Path("fixtures")
    fixtures_dir.mkdir(exist_ok=True)

    notes_path = fixtures_dir / "notes.jsonl"
    truth_path = fixtures_dir / "ground_truth.jsonl"

    label_counts: Counter = Counter()
    total_entities = 0

    with open(notes_path, "w") as nf, open(truth_path, "w") as tf:
        for i in range(args.count):
            template = random.choice(TEMPLATES)
            phi = generate_phi()
            text, entities = render_note(template["text"], phi)

            note_id = f"{i:04d}"

            nf.write(
                json.dumps({"note_id": note_id, "type": template["type"], "text": text})
                + "\n"
            )
            tf.write(
                json.dumps({"note_id": note_id, "entities": entities}) + "\n"
            )

            for e in entities:
                label_counts[e["label"]] += 1
            total_entities += len(entities)

    print(f"Generated {args.count} notes -> {notes_path}, {truth_path}")
    print(f"Total entities: {total_entities}")
    print("\nEntity type distribution:")
    for label, count in sorted(label_counts.items(), key=lambda x: -x[1]):
        print(f"  {label:25s} {count:5d}")


if __name__ == "__main__":
    main()
