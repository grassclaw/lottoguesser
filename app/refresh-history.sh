#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$ROOT/work"

mkdir -p "$WORK"

curl -L https://files.arizonalottery.com/past-180-days/Past180Days_The_Pick.pdf -o "$WORK/Past180Days_The_Pick.pdf"
curl -L https://files.arizonalottery.com/past-180-days/Past180Days_Fantasy_5.pdf -o "$WORK/Past180Days_Fantasy_5.pdf"
curl -L https://files.arizonalottery.com/past-180-days/Past180Days_Triple_Twist.pdf -o "$WORK/Past180Days_Triple_Twist.pdf"

pdftotext -layout "$WORK/Past180Days_The_Pick.pdf" "$WORK/Past180Days_The_Pick.txt"
pdftotext -layout "$WORK/Past180Days_Fantasy_5.pdf" "$WORK/Past180Days_Fantasy_5.txt"
pdftotext -layout "$WORK/Past180Days_Triple_Twist.pdf" "$WORK/Past180Days_Triple_Twist.txt"

node "$WORK/parse-az-lottery.mjs"
cp "$WORK/az-lottery-history.js" "$ROOT/outputs/az-lottery-history.js"

echo "Updated $ROOT/outputs/az-lottery-history.js"
