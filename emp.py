#!/usr/bin/env python3
# Run this in Python 3.

# Author: Vaddadi Kartick
# Released under Apache license 2.0.

# This script tells you whether you're better off as an employee or consultant, based on Indian tax
# laws, for a given level of gross income.
#
# Assumptions:
#  0) You pay GST. Many consultants don't, so check that you do before you continue with this
#     script.
#  1) You're paid a certain amount of money, and you have to pay all taxes out of it, including GST
#     -- you can't pass the GST along by grossing it up.
#  2) This is for fiscal year 2018-19.
#  3) You're a resident individual of India, not a company.
#  4) You're not a senior citizen.
#  5) Numbers are annual, and in thousands of rupees, except when stated otherwise.
#  6) This script doesn't take into account the cost in your time of dealing with the bureaucratic
#     GST regime, or the cost of hiring a CA to do so.
#  7) GST paid can't be set off against something else.

# Reference: https://www.bankbazaar.com/tax/income-tax-slabs.html


import math

PRESUMPTIVE_RATE = .5
# Consultants benefit from presumptive taxation  at this rate. Change it if you fall under a
# different slab. Read up on presumptive taxation at https://cleartax.in/s/sugam-itr-4s-form

EMPLOYEE_TAX_DEDUCTION = 160
# Deductions you can claim if you’re an employee, but not if you're a consultant. This includes
# section 80C, 80D medical insurance, and so on. Change it as suitable.

GST_RATE = .18
# What GST rate do you fall under? Change it as suitable. If you don't pay GST at all — neither you
# nor the entity paying you is registered under GST — set this to 0. Or if you're exporting, which
# is zero-rated, set this to 0.

SLAB_1 = 250
SLAB_2 = 500
SLAB_3 = 1000

# How much income tax is due under slab 1?
def income_tax_slab_1(income):
  if income <= SLAB_1:
    return 0
  if income > SLAB_2:
    income = SLAB_2
  income -= SLAB_1
  return income * .05  # 5%

# How much income tax is due under slab 2?
def income_tax_slab_2(income):
  if income <= SLAB_2:
    return 0
  if income > SLAB_3:
    income = SLAB_3
  income -= SLAB_2
  return income * .2  # 20%

# How much income tax is due under slab 3?
def income_tax_slab_3(income):
  if income <= SLAB_3:
    return 0
  income -= SLAB_3
  return income * .3  #30%

# How much income tax is due?
def incomeTaxFor(income):
  tax = income_tax_slab_1(income) + income_tax_slab_2(income) + income_tax_slab_3(income)
  if income <= 350:
    tax = min(tax, 2.5)  # If you earn < 3.5 lac, your tax is limited to ₹2500.
  if income >= 50 * 100:
    print("Warning: ignoring surcharge for high income")
  return tax * 1.04  # Health and education cess

# How much tax does an employee pay for the given income?
def taxForEmployee(income):
  return incomeTaxFor(income - EMPLOYEE_TAX_DEDUCTION)

# How much tax does a consultant pay for the given income?
def taxForConsultant(income):
  EFFECTIVE_GST_RATE = GST_RATE/(1 + GST_RATE)
  # If you earn ₹100 on which you need to pay GST from your own pocket, you pay around ₹15, not ₹18.
  # Don't change this formula.

  gst = income * EFFECTIVE_GST_RATE
  income -= gst  # Income tax is net of GST.
  income *= PRESUMPTIVE_RATE
  return incomeTaxFor(income) + gst

def monthlyInHandForEmployee(income):
  return math.floor((income - taxForEmployee(income)) / 12)

def monthlyInHandForConsultant(income):
  return math.floor((income - taxForConsultant(income)) / 12)

def calculateAndPrint(income):
  in_hand_employee = monthlyInHandForEmployee(income)
  in_hand_consultant = monthlyInHandForConsultant(income)
  print(f"An employee earns ₹{in_hand_employee}K, while a consultant earns ₹{in_hand_consultant}K, in hand each month.")

calculateAndPrint(10 * 100)
