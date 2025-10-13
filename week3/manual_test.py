"""
Simple manual test - Opens browser and waits for you to test manually
This lets you see the real behavior step by step
"""
import asyncio
from playwright.async_api import async_playwright
import time

async def manual_test():
    """Open browser and let user test manually"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        print("=" * 80)
        print("MANUAL TESTING WINDOW")
        print("=" * 80)
        print("\n🌐 Opening Streamlit app...")
        await page.goto("http://localhost:8503")
        await page.wait_for_timeout(3000)
        
        print("\n✅ App loaded!")
        print("\n" + "=" * 80)
        print("TESTING INSTRUCTIONS")
        print("=" * 80)
        
        print("\n📋 STEP 1: Check Initial State")
        print("   - Look at sidebar for 'Agent Status' section")
        print("   - Should see 4 agents in 'Idle' state")
        print("   - Press Enter when ready...")
        input()
        
        # Get sidebar content
        sidebar = page.locator('[data-testid="stSidebar"]')
        sidebar_text = await sidebar.inner_text()
        print(f"\n📊 Current Sidebar:\n{sidebar_text}\n")
        
        print("\n📋 STEP 2: Enable Real APIs")
        print("   - Check the 'Use Real APIs' checkbox")
        print("   - Press Enter when done...")
        input()
        
        print("\n📋 STEP 3: Submit First Query")
        print("   - Type: 'Find information about vacation policy'")
        print("   - Press Enter to submit")
        print("   - Watch the Agent Status section update")
        print("   - Press Enter here when query completes...")
        input()
        
        # Check sidebar after first query
        sidebar_text_1 = await sidebar.inner_text()
        print(f"\n📊 Sidebar After First Query:\n{sidebar_text_1}\n")
        await page.screenshot(path="week3/manual_test_query1.png")
        print("📸 Screenshot saved: manual_test_query1.png")
        
        print("\n📋 STEP 4: Submit Second Query")
        print("   - Type: 'How many vacation days do I get?'")
        print("   - Press Enter to submit")
        print("   - ⚠️  WATCH CAREFULLY:")
        print("      * Do the timestamps change?")
        print("      * Do the states update again?")
        print("      * Does Recent Activity reset/update?")
        print("   - Press Enter here when query completes...")
        input()
        
        # Check sidebar after second query
        sidebar_text_2 = await sidebar.inner_text()
        print(f"\n📊 Sidebar After Second Query:\n{sidebar_text_2}\n")
        await page.screenshot(path="week3/manual_test_query2.png")
        print("📸 Screenshot saved: manual_test_query2.png")
        
        # Compare
        print("\n" + "=" * 80)
        print("COMPARISON: Query 1 vs Query 2")
        print("=" * 80)
        
        if sidebar_text_1 == sidebar_text_2:
            print("❌ PROBLEM: Sidebar text is IDENTICAL")
            print("   This means timestamps/states didn't update!")
        else:
            print("✅ GOOD: Sidebar text changed")
            
        print("\n📋 STEP 5: Submit Third Query")
        print("   - Type: 'Can I carry over vacation days?'")
        print("   - Press Enter to submit")
        print("   - Again, watch for updates")
        print("   - Press Enter here when query completes...")
        input()
        
        # Check sidebar after third query
        sidebar_text_3 = await sidebar.inner_text()
        print(f"\n📊 Sidebar After Third Query:\n{sidebar_text_3}\n")
        await page.screenshot(path="week3/manual_test_query3.png")
        print("📸 Screenshot saved: manual_test_query3.png")
        
        # Final comparison
        print("\n" + "=" * 80)
        print("FINAL ANALYSIS")
        print("=" * 80)
        
        if sidebar_text_1 == sidebar_text_2 == sidebar_text_3:
            print("❌ MAJOR ISSUE: All three queries show identical sidebar!")
            print("   Problem: States/timestamps are frozen after first query")
        elif sidebar_text_2 == sidebar_text_3:
            print("⚠️  ISSUE: Second and third queries show same sidebar")
            print("   Problem: Updates stopped after second query")
        else:
            print("✅ SUCCESS: Each query updated the sidebar")
        
        print("\n📸 Screenshots saved:")
        print("   - manual_test_query1.png")
        print("   - manual_test_query2.png")  
        print("   - manual_test_query3.png")
        
        print("\n⏸️  Browser will stay open. Press Enter to close...")
        input()
        
        await browser.close()

if __name__ == "__main__":
    print("🚀 Starting Manual Test Session...\n")
    print("This will open a browser and guide you through testing.\n")
    asyncio.run(manual_test())
    print("\n✅ Manual test session complete!")
