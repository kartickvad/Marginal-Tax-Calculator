#!/usr/bin/env python3
# coding: utf-8
# Run this in the latest version of Python. I tested with 3.7.

# Author: Kartick Vaddadi
# Released under Apache license 2.0.


# This script handles
#   - Income tax
#   - Professional tax


# This script calculates take-home pay for a given CTC, for a consultant.
#
# Assumptions:
#  - This is for fiscal year 2019-20.
#  - You're a resident individual of India, not a company.
#  - You're not a senior citizen.
#  - Numbers are annual, and in thousands of rupees, except when stated otherwise. Take-home pay
#     is always monthly.
#  - This script doesn't take into account the cost in your time of dealing with the bureaucracy
#     regime, or the cost of hiring a CA to do so.
#  - HRA and LTA are ignored.
#  - Professional tax is calculated for Karnataka.
#
# Reference: https://www.bankbazaar.com/tax/income-tax-slabs.html

# All values are in thousands.


import math

# Professionals pay an extra state, which varies from state to state. In Karnataka, it's ₹200 per
# month, except for one month, where it's ₹300.
PROFESSIONAL_TAX = 2.5

# Some consultants benefit from presumptive taxation at this rate. This means that 50% of your
# income is tax-free, and only the remaining 50% is considered taxable income.
#
# But for some people, only 8% of income is considered taxable, in wihch case you should set this
# to 0.08. Others pay 6%.
#
# Read up on presumptive taxation at https://cleartax.in/s/sugam-itr-4s-form. It falls under section
# 44AD and 44ADA.
PRESUMPTIVE_RATE = .5

# The tax slabs are 2.5, 5 and 10 lakh:
SLAB_1 = 250
SLAB_2 = 500
SLAB_3 = 1000

def lakh(amount):
  return amount * 100

# How much income tax is due under slab 1?
def income_tax_slab_1(income):
  if income <= SLAB_1:
    return 0  # No tax under this slab, since your income is too low.
  if income > SLAB_2:
    income = SLAB_2  # Income that falls under the next slab shouldn't be taxed in this one.
  income -= SLAB_1 # Only the part of your income that exceeds the limit is taxed.
  return income * .05  # 5% tax rate for this slab

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
def income_tax_for(income):
  # People with income less than 5 lakh pay no tax, though according to the slabs, they're required
  # to:
  if income <= 500:
    return 0
  tax = income_tax_slab_1(income) + income_tax_slab_2(income) + income_tax_slab_3(income)
  cess = tax * .04  # Health and education cess is 4% of the tax.
  surcharge = 0
  if income >= lakh(100):
    print("Warning: ignoring surcharge for high income")
  if income >= lakh(50):
    surcharge = tax * .1  # 10% of tax
  return tax + cess + surcharge

def income_and_professional_tax_for(income):
  return income_tax_for(income) + PROFESSIONAL_TAX

# Comprises of income tax and professional tax.
def total_tax_for(income):
  income *= PRESUMPTIVE_RATE
  return income_and_professional_tax_for(income)

def take_home(income):
  tax = total_tax_for(income)
  income = income - tax
  return math.floor(income / 12)  # Round to the nearest thousand.
  
def format_money(amount):
  if amount >= 100:
    amount /= 100
    return f"{amount} lakh"
  return f"{amount}K"

def print_take_home_for(income):
  take_home_pay = format_money(take_home(income))
  print(f"For a CTC of {format_money(income)}, you take home {take_home_pay}, each month.")

def ctc_for_take_home_pay(desired_take_home):
  ctc = 1
  while take_home(ctc) < desired_take_home:
    ctc += 1
  return ctc

def print_ctc_for_take_home_pay(desired_take_home):
  ctc = format_money(ctc_for_take_home_pay(desired_take_home))
  print(f"To take home {format_money(desired_take_home)} a month, you should aim for a gross annual income of {ctc}.")
    
print_take_home_for(lakh(10))
print()
print_ctc_for_take_home_pay(50)
