"""The Profile model shows information about the user."""

from __future__ import annotations

from pydantic import BaseModel


class Profile(BaseModel):
    """The profile model shows information about the user."""

    class RelationshipManager(BaseModel):
        """The relationship manager of the user.

        Usually indicates contact details of the employer of the user.
        """

        name: str
        email: str
        phone: str

    class Budget(BaseModel):
        """Indicates all budget information of the user."""

        actualBudgetPerMonth: int
        maxBudgetPerMonth: int
        normBudgetPerMonth: int
        normBudgetGasolinePerMonth: int
        normBudgetElectricPerMonth: int
        maxBudgetGasolinePerMonth: int
        maxBudgetElectricPerMonth: int
        normUndershootPercentage: int
        maxNormUndershootPercentage: int
        savedBudget: int
        savedBudgetPayoutAllowed: bool
        holidayCarRaiseAllowed: bool

    class Address(BaseModel):
        """The address of the user."""

        street: str
        houseNumber: str
        houseNumberAddendum: str
        zipCode: str
        city: str

    class CurrentReservation(BaseModel):
        """The current reservation of the user, if any."""

        externalId: str
        startedAtUtc: str
        vehicleId: str
        vehicleExternalId: str
        hasLicenseCardAvailable: bool

    id: str
    initials: str
    firstName: str
    lastName: str
    phoneNumber: str
    email: str
    customerName: str
    isConsumer: bool
    flexPlus: bool
    relationshipManager: RelationshipManager
    requiresIncludeTaxInPrices: bool
    includeMileageCostsInPricing: bool
    includeFuelCostsInPricing: bool
    onlyShowNetMonthCosts: bool
    numberOfKmPerMonth: int
    remainingSwaps: int
    budget: Budget
    hideIntroPopup: bool
    chargingStationRequest: bool
    pendingCancelation: bool
    pendingBikeCancelation: bool
    pendingBudgetPayout: bool
    pendingHolidayCarRaise: bool
    deliveryAddress: Address
    officialAddress: Address
    currentReservation: CurrentReservation | None = None
    firstReservationAllowedFromUtc: str
    firstDeliveryAllowedFromUtc: str
    canOrderBike: bool
    canMakeReservation: bool
    canMakeReservationFromUtc: str
    canMakePickup: bool
    canMakeBikeReservation: bool
    canMakeBikePickup: bool
    canMakeFirstReservation: bool
    canDecline: bool
    canDeclineBike: bool
