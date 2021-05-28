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

# All values in this script are monthly, and in thousands.

import math

# Professionals pay an extra state, which varies from state to state. In Karnataka, it's ₹200 per
# month, except for one month, where it's ₹300.
PROFESSIONAL_TAX = 2.5 / 12

def lakh(amount):
  return amount * 100

def tax_for(gross_income):
  tax = gross_income * 0.3
  cess = tax * .04  # Health and education cess is 4% of the tax.
  return tax + cess + PROFESSIONAL_TAX

def net_income_for(gross_income):
  return gross_income - tax_for(gross_income)

def gross_income_for(net_income):
  gross_income = 1
  while net_income_for(gross_income) < net_income:
    gross_income += 1
  return gross_income




# I/O related:
def format_money(amount):
  if amount >= 100:
    amount /= 100
    return f"{amount} lakh"
  return f"{amount}K"

def print_net_income_for(gross_income):
  net_income = format_money(math.floor(net_income_for(gross_income)))
  print(f"For a gross income of {format_money(gross_income)}, your net income is {net_income}, both monthly.")

def print_gross_income_for(net_income):
  gross_income = format_money(gross_income_for(net_income))
  print(f"For a net income of {format_money(net_income)}, you should aim for a gross income of {gross_income}, both monthly.")
    
print_net_income_for(lakh(1))
print()
print_gross_income_for(50)
