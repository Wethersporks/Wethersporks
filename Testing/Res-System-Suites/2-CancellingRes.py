"""Cancelling a Reservation"""

# UC2-1A: Click the 'Cancel Reservation' link within a confirmation email where the reservation is more than 2 hours away from the current datetime
# and has not been cancelled already
# -> Cancellation passes, reservation is cancelled in the database and user is notified of a successful cancellation and is given cancellation email

# UC2-1B: Click the 'Cancel Reservation' link within a confirmation email where the reservation is with 2 hours from the current datetime
# -> Cancellation fails, user is notified that the reservation cannot be cancelled

# UC2-1C: Click the 'Cancel Reservation' link within a confirmation email where the reservation is before the current datetime
# -> Cancellation fails, user is notified that the reservation cannot be cancelled

# UC2-1D: Click the 'Cancel Reservation' link within a confirmation email where the reservation is more than 2 hours away from the current datetime
# and has been cancelled already
# -> Cancellation fails, user is notified that the reservation has already been cancelled

# UC2-1E: Manually input a cancellation URL into the web browser with a token of "0"
# -> Cancellation fails, user is notified that the reservation cannot be found