# Neighborhood pickup desk

## Problem and User
Shift volunteers use one shared parcel list.

## Intended Outcome and Value
Show a volunteer what can be handed out and what has already left.

## Find a topic
- Pickup list, completed pickups, shift change: [shift handoff](shift-handoff.md). Implementation: `desk.py:pickup_list`.
- Badge colors: `desk.py:badge`; checks in `test_desk.py`.

## Scope
The local list and its labels. No account or shipment tracking.

## Constraints and Assumptions
Volunteers hand the desk over in person.

## Success Criteria
A volunteer can distinguish ready parcels from completed pickups.

## Current Promise
- Stage: Working
- Version: V1
- Version goal: clear shift handoff
- Exit evidence: local Python checks
