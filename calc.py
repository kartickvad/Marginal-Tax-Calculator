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
#  - Your income from other clients is enough to put you in the 30% slab, so each marginal rupee is
#    taxed at 30%.
#  - Your income does not exceed 50 lakh, so surcharge does not apply.
#
# Reference: https://www.bankbazaar.com/tax/income-tax-slabs.html

# All values in this script are in thousands.

import math

# Professionals pay an extra state, which varies from state to state. In Karnataka, it's ₹200 per
# month, except for one month, where it's ₹300.
PROFESSIONAL_TAX = 2.5

def lakh(amount):
  return amount * 100

# How much income tax is due?
def income_tax_for(income):
  tax = income * 0.3
  cess = tax * .04  # Health and education cess is 4% of the tax.
  if income >= lakh(50):
    print("Warning: ignoring surcharge for high income")
  return tax + cess

def income_and_professional_tax_for(income):
  return income_tax_for(income) + PROFESSIONAL_TAX

def take_home(income):
  tax = income_and_professional_tax_for(income)
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
