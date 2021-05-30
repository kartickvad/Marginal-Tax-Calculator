#!/usr/bin/env python3
# coding: utf-8

"""
Author: Kartick Vaddadi
Released under Apache license 2.0.

This script calculates marginal tax for consultants: if you want to earn a given amount of net
income, how much gross fee should you quote a client, considering income tax and professional
tax? And if you already have a client for a given gross fee, how much net income will you earn
from it?

Assumptions:
 - This is for fiscal year 2021-22.
 - You're a resident individual of India or an LLP.
 - You're not a senior citizen.
 - Professional tax is calculated for Karnataka.
 - Your income from other clients is enough to put you in the 30% slab, so each marginal rupee is
   taxed at 30%.
 - Your income does not exceed 50 lakh, so surcharge does not apply.
 - GST is not included because it's zero-rated for foreign clients. (Even for Indian clients,
   it's typically passed on to clients over and above the quoted fee).
"""

# Varies from state to state. In Karnataka, it's ₹200 per month, except for one month, where it's
# ₹300.
PROFESSIONAL_TAX = 2500 / 12

# 30% with 4% health and education cess.
INCOME_TAX_RATE = 0.3 * 1.04
  
def total_tax_for(gross_income):
  "Calculates income and professional tax for the given gross income"
  taxable_income = gross_income - PROFESSIONAL_TAX  # You don't pay income tax on professional tax.
  income_tax = taxable_income * INCOME_TAX_RATE
  return income_tax + PROFESSIONAL_TAX

def net_income_for(gross_income):
  "Calculates net income (what remains after tax) for the given gross income"
  return gross_income - total_tax_for(gross_income)

def gross_income_for(net_income):
  "If you want to earn a given net income, how much gross income should you quote to a client?"
  gross_income = 1
  while net_income_for(gross_income) < net_income:
    gross_income += 1
  return gross_income




# I/O related:
def format_rupees(amount):
  return f"₹{amount}"

def print_gross_income_for(net_income):
  gross_income = gross_income_for(net_income)
  print(f"For a net income of {format_rupees(net_income)}, you should aim for a gross income of {format_rupees(gross_income)}, both monthly.")

print_gross_income_for(160664)
