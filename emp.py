#!/usr/bin/env python3
# Run this in Python 3.

# Author: Vaddadi Kartick
# Released under Apache license 2.0.

# This script calculates take-home pay for a given CTC, for both an employee and a consultant.
#
# Assumptions:
#  1) GST comes out of your pocket — you can't pass the GST along by grossing it up.
#  2) This is for fiscal year 2018-19.
#  3) You're a resident individual of India, not a company.
#  4) You're not a senior citizen.
#  5) Numbers are annual, and in thousands of rupees, except when stated otherwise.
#  6) This script doesn't take into account the cost in your time of dealing with the bureaucratic
#     GST regime, or the cost of hiring a CA to do so.
#  7) GST paid can't be set off against something else.
#  8) HRA and LTA are ignored.
#
# Reference: https://www.bankbazaar.com/tax/income-tax-slabs.html


import math

# 25.61% of CTC goes to PF and pension. Set this to zero if you don't want to consider this, for an
# employee.
PF_RATE = .2561

PROFESSIONAL_TAX = 2.5

PRESUMPTIVE_RATE = .5
# Consultants benefit from presumptive taxation  at this rate. Change it if you fall under a
# different slab. Read up on presumptive taxation at https://cleartax.in/s/sugam-itr-4s-form

EMPLOYEE_TAX_DEDUCTION = 160
# Deductions you can claim if you’re an employee, but not if you're a consultant. This includes
# section 80C, 80D medical insurance, and so on. Change it as suitable.

GST_RATE = 0
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
  if income <= 500:
    return 0
  tax = income_tax_slab_1(income) + income_tax_slab_2(income) + income_tax_slab_3(income)
  if income >= 50 * 100:
    print("Warning: ignoring surcharge for high income")
  return tax * 1.04  # Health and education cess

# How much tax does an employee pay for the given income?
def taxForEmployee(income):
  return incomeTaxFor(income - EMPLOYEE_TAX_DEDUCTION) + PROFESSIONAL_TAX

# How much tax does a consultant pay for the given income?
def taxForConsultant(income):
  EFFECTIVE_GST_RATE = GST_RATE/(1 + GST_RATE)
  # If you earn ₹100 on which you need to pay GST from your own pocket, you pay around ₹15, not ₹18.
  # Don't change this formula.

  gst = income * EFFECTIVE_GST_RATE
  income -= gst  # Income tax is net of GST.
  income *= PRESUMPTIVE_RATE
  return incomeTaxFor(income) + gst + PROFESSIONAL_TAX

def monthlyTakeHomeForEmployee(income):
  tax = taxForEmployee(income)
  pf = income * PF_RATE
  income = income - tax - pf
  return math.floor(income / 12)

def monthlyTakeHomeForConsultant(income):
  tax = taxForConsultant(income)
  income -= tax
  return math.floor(income / 12)
  
def formatMoney(amount):
  if amount >= 100:
    amount /= 100
    return f"{amount} lac"
  return f"{amount}K"

def calculateAndPrint(income):
  in_hand_employee = formatMoney(monthlyTakeHomeForEmployee(income))
  in_hand_consultant = formatMoney(monthlyTakeHomeForConsultant(income))
  print(f"For a CTC of {formatMoney(income)}, an employee takes home {in_hand_employee}, while a consultant takes home {in_hand_consultant}, each month.")

calculateAndPrint(12 * 100)
