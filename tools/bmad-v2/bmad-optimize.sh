#!/bin/bash
# BMAD v2 Optimization Script
# Unified optimization workflow using agents and automation

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
FILE=$1
MAX_TIER=${2:-4}  # Default to Tier 4
AUTO_FIX=${3:-true}

# Check arguments
if [ -z "$FILE" ]; then
    echo "Usage: ./bmad-optimize.sh <file.html> [max_tier] [auto_fix]"
    echo ""
    echo "Examples:"
    echo "  ./bmad-optimize.sh index.html           # Run Tiers 1-4 with auto-fix"
    echo "  ./bmad-optimize.sh index.html 2         # Run only Tiers 1-2"
    echo "  ./bmad-optimize.sh index.html 4 false   # Run Tiers 1-4, no auto-fix"
    exit 1
fi

# Check file exists
if [ ! -f "$FILE" ]; then
    echo -e "${RED}❌ File not found: $FILE${NC}"
    exit 1
fi

# Print header
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 BMAD v2 OPTIMIZATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   File: $FILE"
echo "   Max Tier: $MAX_TIER"
echo "   Auto-fix: $AUTO_FIX"
echo "   Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 1: Create backup
BACKUP_FILE="${FILE}.backup_$(date +%Y%m%d_%H%M%S)"
echo -e "${BLUE}📦 Step 1: Creating backup...${NC}"
cp "$FILE" "$BACKUP_FILE"
echo -e "${GREEN}   ✅ Backup created: $BACKUP_FILE${NC}"
echo ""

# Function to run a tier
run_tier() {
    local tier=$1
    local tier_name=$2
    local params=$3
    local target=$4
    local required=$5

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎯 TIER $tier: $tier_name ($params params) - Target: $target%"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # Run Python agent coordinator for this tier
    if [ "$AUTO_FIX" = "true" ]; then
        python tools/bmad-v2/agent-coordinator.py "$FILE" "$tier"
    else
        python tools/bmad-v2/agent-coordinator.py "$FILE" "$tier" --no-fix
    fi

    # Get score from last run
    SCORE=$(python tools/bmad-v2/get-score.py "$FILE" "$tier" 2>/dev/null || echo "0")

    echo ""
    echo -e "${BLUE}   📊 TIER $tier RESULT: $SCORE/100${NC}"

    # Check gates
    if [ "$tier" = "1" ] && [ "$SCORE" -lt 100 ]; then
        echo -e "${RED}   🔴 GATE 1 FAILED: Tier 1 must be 100%${NC}"
        echo -e "${RED}   🔴 BLOCKING DEPLOYMENT${NC}"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo -e "${RED}❌ OPTIMIZATION FAILED AT TIER 1${NC}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        exit 1
    fi

    if [ "$tier" = "2" ]; then
        if [ "$SCORE" -ge 85 ]; then
            echo -e "${GREEN}   ✅ GATE 2 PASSED: Excellent SEO+CRO${NC}"
        elif [ "$SCORE" -ge 80 ]; then
            echo -e "${YELLOW}   ⚠️  GATE 2 WARNING: Score 80-84% (target: 85%+)${NC}"
        else
            echo -e "${YELLOW}   ⚠️  GATE 2 WARNING: Score below 80%${NC}"
        fi
    fi

    if [ "$SCORE" -ge "$target" ]; then
        echo -e "${GREEN}   ✅ Target achieved ($target%)${NC}"
    else
        echo -e "${YELLOW}   ⚠️  Below target (goal: $target%)${NC}"
    fi

    echo ""

    # Return score
    echo "$SCORE"
}

# Tier definitions
TIER1_SCORE=0
TIER2_SCORE=0
TIER3_SCORE=0
TIER4_SCORE=0

# Run Tier 1 (always required)
if [ "$MAX_TIER" -ge 1 ]; then
    TIER1_SCORE=$(run_tier 1 "Critical Foundation" 15 100 true)
fi

# Run Tier 2 (if requested)
if [ "$MAX_TIER" -ge 2 ]; then
    TIER2_SCORE=$(run_tier 2 "SEO + CRO Core" 30 85 false)
fi

# Run Tier 3 (if requested)
if [ "$MAX_TIER" -ge 3 ]; then
    TIER3_SCORE=$(run_tier 3 "Content + Basic UX" 50 70 false)
fi

# Run Tier 4 (if requested)
if [ "$MAX_TIER" -ge 4 ]; then
    TIER4_SCORE=$(run_tier 4 "Performance + Speed" 25 80 false)
fi

# Final Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 OPTIMIZATION COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   📈 Final Scores:"
if [ "$MAX_TIER" -ge 1 ]; then
    if [ "$TIER1_SCORE" -eq 100 ]; then
        echo -e "      Tier 1: ${GREEN}$TIER1_SCORE/100 ✅${NC} (Critical - REQUIRED)"
    else
        echo -e "      Tier 1: ${RED}$TIER1_SCORE/100 ❌${NC} (Critical - REQUIRED)"
    fi
fi

if [ "$MAX_TIER" -ge 2 ]; then
    if [ "$TIER2_SCORE" -ge 85 ]; then
        echo -e "      Tier 2: ${GREEN}$TIER2_SCORE/100 ✅${NC} (SEO+CRO - Target: 85%)"
    elif [ "$TIER2_SCORE" -ge 80 ]; then
        echo -e "      Tier 2: ${YELLOW}$TIER2_SCORE/100 ⚠️${NC}  (SEO+CRO - Target: 85%)"
    else
        echo -e "      Tier 2: ${YELLOW}$TIER2_SCORE/100 ⚠️${NC}  (SEO+CRO - Target: 85%)"
    fi
fi

if [ "$MAX_TIER" -ge 3 ]; then
    if [ "$TIER3_SCORE" -ge 70 ]; then
        echo -e "      Tier 3: ${GREEN}$TIER3_SCORE/100 ✅${NC} (Content+UX - Target: 70%)"
    else
        echo -e "      Tier 3: ${BLUE}$TIER3_SCORE/100 ℹ️${NC}  (Content+UX - Target: 70%)"
    fi
fi

if [ "$MAX_TIER" -ge 4 ]; then
    if [ "$TIER4_SCORE" -ge 80 ]; then
        echo -e "      Tier 4: ${GREEN}$TIER4_SCORE/100 ✅${NC} (Performance - Target: 80%)"
    else
        echo -e "      Tier 4: ${BLUE}$TIER4_SCORE/100 ℹ️${NC}  (Performance - Target: 80%)"
    fi
fi

echo ""
echo "   📁 Backup: $BACKUP_FILE"
echo ""

# Deployment decision
if [ "$TIER1_SCORE" -eq 100 ]; then
    if [ "$TIER2_SCORE" -ge 85 ] || [ "$MAX_TIER" -lt 2 ]; then
        echo -e "   ${GREEN}✅ DEPLOYMENT STATUS: APPROVED${NC}"
        echo "      → All gates passed"
        echo "      → Ready for production"
        EXIT_CODE=0
    elif [ "$TIER2_SCORE" -ge 80 ]; then
        echo -e "   ${YELLOW}⚠️  DEPLOYMENT STATUS: APPROVED WITH WARNING${NC}"
        echo "      → Tier 1 passed (100%)"
        echo "      → Tier 2 acceptable but below target (${TIER2_SCORE}% vs 85%)"
        echo "      → Consider improving Tier 2 before deployment"
        EXIT_CODE=0
    else
        echo -e "   ${YELLOW}⚠️  DEPLOYMENT STATUS: NOT RECOMMENDED${NC}"
        echo "      → Tier 1 passed (100%)"
        echo "      → Tier 2 below acceptable threshold (${TIER2_SCORE}% vs 80%)"
        echo "      → Improve Tier 2 parameters before deployment"
        EXIT_CODE=1
    fi
else
    echo -e "   ${RED}🔴 DEPLOYMENT STATUS: BLOCKED${NC}"
    echo "      → Tier 1 failed (${TIER1_SCORE}% vs 100% required)"
    echo "      → Fix Tier 1 critical issues before deployment"
    EXIT_CODE=1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

exit $EXIT_CODE
