#!/usr/bin/env python3.6
# Run this in Python 3.6.

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
#  2) Your income is < 50 lac. This script doesn't take surcharges into account.
#  3) This is for fiscal year 2017-18.
#  4) You're a resident individual of India, not a company.
#  5) You're not a senior citizen.
#  6) This doesn't take into account the rebate of up to ₹2500 for low income earners.
#  7) All numbers are annual.
#  8) This script doesn't take into account the cost in your time of dealing with the bureaucratic
#     GST regime, or the cost of hiring a CA to do so.
#  9) GST paid can't be set off against something else.

PRESUMPTIVE_RATE = .5
# Your presumptive taxation applies at this rate. Change it if you fall under a different slab.
# Read up on presumptive taxation at https://cleartax.in/s/sugam-itr-4s-form

EMPLOYEE_TAX_DEDUCTION = 160 * 1000
# Deductions you can claim if you’re an employee, but not if you're a consultant. This includes
# section 80C, 80D medical insurance, and so on. Change it as suitable.

GST_RATE = .18
# What GST rate do you fall under? Change it as suitable. If you don't pay GST at all — neither you
# nor the entity paying you is registered under GST — set this to 0. Or if you're exporting, which
# is zero-rated, set this to 0.

EFFECTIVE_GST_RATE = GST_RATE/(1 + GST_RATE)
# If you earn ₹100 on which you need to pay GST from your own pocket, you pay around ₹15, not ₹18.
# Don't change this formula.

SLAB_1 = 250 * 1000
SLAB_2 = 500 * 1000
SLAB_3 = 1000 * 1000

# How much income tax is due under slab 1?
def income_tax_slab_1(income):
  if income <= SLAB_1:
    return 0
  if income > SLAB_2:
    income = SLAB_2
  income -= SLAB_1
  return income * .05

# How much income tax is due under slab 2?
def income_tax_slab_2(income):
  if income <= SLAB_2:
    return 0
  if income > SLAB_3:
    income = SLAB_3
  income -= SLAB_2
  return income * .2

# How much income tax is due under slab 3?
def income_tax_slab_3(income):
  if income <= SLAB_3:
    return 0
  income -= SLAB_3
  return income * .3

# How much income tax is due?
def incomeTaxFor(income):
  tax = income_tax_slab_1(income) + income_tax_slab_2(income) + income_tax_slab_3(income)
  return tax * 1.03  # Cess

# How much tax does an employee pay for the given income?
def taxForEmployee(income):
  return incomeTaxFor(income - EMPLOYEE_TAX_DEDUCTION)

# How much tax does a consultant pay for the given income?
def taxForConsultant(income):
  gst = income * EFFECTIVE_GST_RATE
  income -= gst  # Income tax is net of GST.
  income *= PRESUMPTIVE_RATE
  return incomeTaxFor(income) + gst

print("The first column is your income (in ₹ lac) , and the second is the extra tax paid by an employee over a consultant (in ₹ thousand):")

# i is income in lacs. Stop before 50, because a surcharge applies at 50.
for i in range(1, 50):
  income = i * 100 * 1000
  employee_tax = taxForEmployee(income)
  consultant_tax = taxForConsultant(income)
  extra = employee_tax - consultant_tax
  extra /= 1000  # Thousands.
  extra = round(extra)
  print(f"{i}, {extra}")
