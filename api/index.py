"""Vercel serverless entry for the breeding-chat demo.

Re-exports the stdlib Handler from app.py — Vercel's Python runtime accepts
a BaseHTTPRequestHandler subclass named `handler`. All routing, data files
and the deterministic compose fallback live in app.py; this file only
adapts the import path.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from app import Handler

handler = Handler
