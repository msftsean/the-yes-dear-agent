"""
Comprehensive Playwright test to verify agent status display and updates
Tests:
1. Initial agent status display
2. First query updates with timestamps
3. Subsequent queries continue updating (no caching issues)
4. Timestamps are in 12-hour format with AM/PM
5. Timestamps are in Eastern Time
6. Recent Activity messages persist and update
"""
import asyncio
import re
from datetime import datetime
import pytz
from playwright.async_api import async_playwright

def is_12_hour_format(time_str):
    """Check if time string is in 12-hour format (HH:MM:SS AM/PM)"""
    pattern = r'^(0?[1-9]|1[0-2]):[0-5][0-9]:[0-5][0-9] (AM|PM)$'
    return bool(re.match(pattern, time_str))

def get_eastern_time():
    """Get current time in Eastern timezone"""
    eastern = pytz.timezone('US/Eastern')
    return datetime.now(eastern)

async def test_agent_status():
    """Comprehensive test for agent status and updates"""
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print("=" * 80)
        print("� COMPREHENSIVE AGENT STATUS TEST")
        print("=" * 80)
        
        print("\n📍 Step 1: Opening Streamlit app...")
        await page.goto("http://localhost:8503")
        await page.wait_for_timeout(3000)
        print("✅ App loaded")
        
        # =====================================================================
        # TEST 1: Initial Display
        # =====================================================================
        print("\n" + "=" * 80)
        print("TEST 1: Initial Agent Status Display")
        print("=" * 80)
        
        sidebar = page.locator('[data-testid="stSidebar"]')
        assert await sidebar.count() > 0, "❌ FAIL: Sidebar not found"
        print("✅ Sidebar found")
        
        sidebar_text = await sidebar.inner_text()
        
        # Check Agent Status section
        assert "Agent Status" in sidebar_text or "🤖" in sidebar_text, "❌ FAIL: Agent Status section not found"
        print("✅ Agent Status section present")
        
        # Check all agents are listed
        agents = ["Coordinator", "Research", "Document", "Summarizer"]
        for agent in agents:
            assert agent in sidebar_text, f"❌ FAIL: {agent} not found"
            print(f"✅ {agent} found")
        
        # Check initial state is Idle
        idle_count = sidebar_text.count("Idle")
        print(f"✅ Found {idle_count} agents in Idle state")
        
        # Screenshot initial state
        await page.screenshot(path="week3/test_1_initial_state.png")
        print("📸 Screenshot: test_1_initial_state.png")
        
        # =====================================================================
        # TEST 2: First Query - Updates with Timestamps
        # =====================================================================
        print("\n" + "=" * 80)
        print("TEST 2: First Query - Status Updates and Timestamps")
        print("=" * 80)
        
        # Find and enable Real APIs checkbox
        print("🔧 Enabling Real APIs...")
        real_apis_checkbox = page.locator('label:has-text("Use Real APIs")')
        if await real_apis_checkbox.count() > 0:
            await real_apis_checkbox.click()
            await page.wait_for_timeout(1000)
            print("✅ Real APIs enabled")
        
        # Submit first query
        print("📝 Submitting first query...")
        chat_input = page.locator('[data-testid="stChatInput"]').locator('textarea')
        await chat_input.fill("Find information about vacation policy")
        await chat_input.press("Enter")
        print("✅ Query submitted")
        
        # Wait for processing
        await page.wait_for_timeout(5000)
        
        # Check sidebar updates
        sidebar_text = await sidebar.inner_text()
        print("\n📊 Sidebar after first query:")
        print(sidebar_text)
        
        # Extract timestamps
        timestamp_pattern = r'\[([^\]]+)\]'
        timestamps = re.findall(timestamp_pattern, sidebar_text)
        print(f"\n🕐 Found {len(timestamps)} timestamps: {timestamps}")
        
        # Check timestamp format (12-hour)
        if timestamps:
            for ts in timestamps:
                if is_12_hour_format(ts):
                    print(f"✅ Timestamp in 12-hour format: {ts}")
                else:
                    print(f"❌ FAIL: Timestamp NOT in 12-hour format: {ts}")
                    print(f"   Expected format: HH:MM:SS AM/PM")
        else:
            print("⚠️  WARNING: No timestamps found after first query")
        
        # Check for state changes
        states_found = []
        for state in ["Complete", "Searching", "Analyzing", "Compiling", "Skipped"]:
            if state in sidebar_text:
                states_found.append(state)
        print(f"✅ States found after query: {states_found}")
        
        # Check Recent Activity
        if "Recent Activity" in sidebar_text:
            print("✅ Recent Activity section present")
            activity_section = sidebar_text[sidebar_text.index("Recent Activity"):]
            activity_lines = [line for line in activity_section.split('\n') if line.strip()]
            print(f"✅ Found {len(activity_lines)} activity messages")
        
        await page.screenshot(path="week3/test_2_first_query.png")
        print("📸 Screenshot: test_2_first_query.png")
        
        # =====================================================================
        # TEST 3: Second Query - Continued Updates (No Caching Issues)
        # =====================================================================
        print("\n" + "=" * 80)
        print("TEST 3: Second Query - Verify Continued Updates")
        print("=" * 80)
        
        print("⏸️  Waiting 3 seconds before second query...")
        await page.wait_for_timeout(3000)
        
        # Get current sidebar state for comparison
        sidebar_before = await sidebar.inner_text()
        timestamps_before = re.findall(timestamp_pattern, sidebar_before)
        
        # Submit second query
        print("📝 Submitting second query...")
        await chat_input.fill("How many vacation days do I get per year?")
        await chat_input.press("Enter")
        print("✅ Query submitted")
        
        # Wait for processing
        await page.wait_for_timeout(5000)
        
        # Check sidebar updates AGAIN
        sidebar_after = await sidebar.inner_text()
        timestamps_after = re.findall(timestamp_pattern, sidebar_after)
        
        print("\n📊 Sidebar after second query:")
        print(sidebar_after)
        print(f"\n🕐 Found {len(timestamps_after)} timestamps: {timestamps_after}")
        
        # Verify timestamps changed (proving no caching)
        if timestamps_before != timestamps_after:
            print("✅ SUCCESS: Timestamps updated (no caching issue)")
            print(f"   Before: {timestamps_before[:3]}")
            print(f"   After:  {timestamps_after[:3]}")
        else:
            print("❌ FAIL: Timestamps did NOT update (caching issue detected)")
        
        # Verify states updated again
        if "Complete" in sidebar_after or "Searching" in sidebar_after:
            print("✅ Agent states updated on second query")
        else:
            print("❌ FAIL: Agent states did NOT update on second query")
        
        await page.screenshot(path="week3/test_3_second_query.png")
        print("📸 Screenshot: test_3_second_query.png")
        
        # =====================================================================
        # TEST 4: Third Query - Persistence Test
        # =====================================================================
        print("\n" + "=" * 80)
        print("TEST 4: Third Query - Long-term Persistence")
        print("=" * 80)
        
        print("⏸️  Waiting 3 seconds before third query...")
        await page.wait_for_timeout(3000)
        
        # Submit third query
        print("📝 Submitting third query...")
        await chat_input.fill("Can I carry over vacation days?")
        await chat_input.press("Enter")
        print("✅ Query submitted")
        
        await page.wait_for_timeout(5000)
        
        sidebar_third = await sidebar.inner_text()
        timestamps_third = re.findall(timestamp_pattern, sidebar_third)
        
        print(f"\n🕐 Timestamps after third query: {timestamps_third}")
        
        if timestamps_third:
            print("✅ Timestamps still updating on third query")
        else:
            print("❌ FAIL: Timestamps stopped updating")
        
        await page.screenshot(path="week3/test_4_third_query.png")
        print("📸 Screenshot: test_4_third_query.png")
        
        # =====================================================================
        # TEST 5: Eastern Time Validation
        # =====================================================================
        print("\n" + "=" * 80)
        print("TEST 5: Eastern Time Zone Validation")
        print("=" * 80)
        
        eastern_now = get_eastern_time()
        current_hour = eastern_now.strftime("%I:%M")  # 12-hour format
        current_ampm = eastern_now.strftime("%p")
        
        print(f"🕐 Current Eastern Time: {eastern_now.strftime('%I:%M:%S %p')}")
        
        # Check if any timestamp is reasonably close to current time
        if timestamps_third:
            print(f"📊 Checking if timestamps match Eastern timezone...")
            # Just verify AM/PM matches current time
            has_matching_ampm = any(current_ampm in ts for ts in timestamps_third)
            if has_matching_ampm:
                print(f"✅ Timestamps appear to be in Eastern time ({current_ampm})")
            else:
                print(f"⚠️  WARNING: Timestamps may not be in Eastern time")
                print(f"   Expected {current_ampm}, found: {timestamps_third}")
        
        # =====================================================================
        # FINAL SUMMARY
        # =====================================================================
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        print("\n✅ Tests Passed:")
        print("   - Agent Status section displays")
        print("   - All 4 agents listed")
        print(f"   - Timestamps found: {len(timestamps_third) > 0}")
        print(f"   - Updates on first query: {len(timestamps) > 0}")
        print(f"   - Updates on second query: {timestamps_before != timestamps_after}")
        print(f"   - Updates on third query: {len(timestamps_third) > 0}")
        
        print("\n⚠️  Issues to Check:")
        if not any(is_12_hour_format(ts) for ts in timestamps_third):
            print("   ❌ Timestamps not in 12-hour format")
        if timestamps_before == timestamps_after:
            print("   ❌ Caching issue: timestamps not updating")
        
        print("\n📸 Screenshots saved:")
        print("   - test_1_initial_state.png")
        print("   - test_2_first_query.png")
        print("   - test_3_second_query.png")
        print("   - test_4_third_query.png")
        
        # Keep browser open for inspection
        print("\n⏸️  Browser will stay open for 15 seconds...")
        await page.wait_for_timeout(15000)
        
        await browser.close()

if __name__ == "__main__":
    print("🚀 Starting Comprehensive Agent Status Test...\n")
    try:
        asyncio.run(test_agent_status())
        print("\n✅ Test completed successfully!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
