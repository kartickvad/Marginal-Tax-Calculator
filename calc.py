#!/usr/bin/env python3
# coding: utf-8
# Run this in the latest version of Python. I tested with 3.9.

# Author: Kartick Vaddadi
# Released under Apache license 2.0.


# This script handles
#   - Income tax
#   - Professional tax


# This script calculates take-home pay for a given CTC, for a consultant.
#
# Assumptions:
#  - This is for fiscal year 2021-22.
#  - You're a resident individual of India or an LLP.
#  - You're not a senior citizen.
#  - Professional tax is calculated for Karnataka.
#  - Your income from other clients is enough to put you in the 30% slab, so each marginal rupee is
#    taxed at 30%.
#  - Your income does not exceed 50 lakh, so surcharge does not apply.
#
# Reference: https://www.bankbazaar.com/tax/income-tax-slabs.html

import math

# Varies from state to state. In Karnataka, it's ₹200 per month, except for one month, where it's
# ₹300.
PROFESSIONAL_TAX = 2500 / 12

LAKH = 100 * 1000

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
  amount = math.floor(amount)
  return f"₹{amount}"

def print_net_income_for(gross_income):
  net_income = format_money(net_income_for(gross_income))
  print(f"For a gross income of {format_money(gross_income)}, your net income is {net_income}, both monthly.")

def print_gross_income_for(net_income):
  gross_income = format_money(gross_income_for(net_income))
  print(f"For a net income of {format_money(net_income)}, you should aim for a gross income of {gross_income}, both monthly.")
    
print_net_income_for(1 * LAKH)
print()
print_gross_income_for(50000)
