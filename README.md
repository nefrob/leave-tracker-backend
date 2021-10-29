# leave-tracker-backend

Tilt Leave Tracker Assignment. See `assignment.md` for details.

The frontend is available on [CodeSandBox](https://codesandbox.io/s/leave-tracker-client-egd6d).

### Usage

Install dependencies and setup the backend package (need `python3` and `pip3`):

```
pip3 install setuptools
python3 setup.py develop
```

Start the backend server with:

```
python3 backend/server.py
```

### Testing

With the backend server running do:

```
python3 -m unittest
```

### Implementation Notes

This project is a full stack implementation of basic leave tracking for employees. A user can schedule leaves given a start and end date up to a maximum allotment of 12 weeks each calendar year (Jan-Dec).

The backend uses Python and Flask to handle the API and the frontend uses Javascript React to handle the UI.

Decisions made:

-   Various api endpoints allow for fetching/updating/creating/deleting leave data from the database. Leaves are not unique, that is two leaves can be scheduled for the same date range. In the future merging overlapping or adjacent leaves would be ideal (the server could respond with a difference set to update the frontend so the leave list doesn't have to be fetched again).
-   Leaves are stored as separate rows instead of a single row for each user due to issues encountered setting up `postgresql` (which supports `ARRAY` data types). This means reading data is less efficient (not continuous) but queries are simpler to understand/write. Furthermore, the remaining yearly leave must be aggregated every time since it cannot be stored in a single location and updated on leave changes. The database is also stored in memory and not persisted to disk (this made development/testing easier).
-   The frontend is written in React and does very simple state management. The `react-datepicker` component isn't great for visualizing the leave calendar, so pre-existing leaves were not marked on it (ideally leaves would be shown on the calendar so entries could be added/adjusted accordingly). The minimum date is set as the current day (or start of the leave period if the leave starts before today and ends on or after). The maximum date is set as the leave start date plus the remaining leave time for that year. If there are sufficient remaining days in the current year to spill into the next then the next year's remaining leave is added as well.
-   The frontend only fetches leaves from the present day on (you cannot browse the leave history). This would be an area to build out (ex. readonly list of past leaves). Furthermore, the state is locked to a single user where a true app with have a login to fetch the correct user profile(s) and perform api queries.
-   The backend does not consider security (no password, authentication, etc.). As this is my first time working with these tools I skipped security for the sake of simplicity. The backend would need to store usernames, password hashes, authenticate users to provide/limit data access, perform rate limiting, validate input, and so on. New endpoints could be made at `/user/login/<string:username>/<string:password_hash>` and `/user/create/<string:username>/<string:password_hash>` and provide user tokens to be used in the frontend.
-   Basic unit testing is written for the backend to test generic cases (ex. does get user list work). Randomization, more complete coverage, error handling and response comparisons would make testing more robust. Integration testing was skipped (omitted for time).
-   The frontend does not have any testing setup (omitted for time).
-   Documentation is minimal on the backend and not present on the frontend. Given more time this could be expanded upon.

### Other

Other code samples can be found at: [@nefrob](https://github.com/nefrob) or on my [portfolio](https://nefrob.github.io/) site.

Some examples:

-   [Python Double Ratchet algorithm](https://github.com/nefrob/double-ratchet-alg)
-   [C++ event-based RPC server](https://github.com/nefrob/cpp-rpc)
-   [Ethereum decentralized token exchange DApp](https://github.com/nefrob/sandman-swap)

### Questions?

Post issues in the [Issue Tracker](https://github.com/nefrob/leave-tracker-backend/issues).
