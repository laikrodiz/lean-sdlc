# Parcel desk shift files

## Problem and User
Volunteers hand parcel records to the next shift. A ticket identifies one parcel.

## Intended Outcome and Value
The incoming shift can reopen a handoff. The coordinator uses the same file for the end-of-day count.

## Scope
Local JSON files only. The pickup desk does not call a remote service.

## Constraints and Assumptions
Handoffs sometimes return from offline desks days later. Received files remain unchanged as the shift record.

## Success Criteria
Opening a shift preserves ticket order and collection status. The end-of-day count agrees with the desk.

## Current Promise
- Stage: Working
- Version: V1
- Version goal: usable shift handoffs
- Exit evidence: local Python tests

## Find a topic
- Save or reopen a shift: `shift_file.py`. A previous shift is in `samples/friday.json`.
- Daily collection count: `end_of_day.py:collected_total`.
