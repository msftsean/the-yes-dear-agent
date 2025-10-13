"""
Quick test to verify real-time agent status updates during query processing
"""
import asyncio
from playwright.async_api import async_playwright
import time

async def test_realtime_updates():
    """Test that agent status updates in real-time, not just at completion"""
    
    async with async_playwright() as p:
        print("\n🚀 Starting real-time update test...")
        
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print("📱 Opening Streamlit app at http://localhost:8507")
        await page.goto("http://localhost:8507", wait_until="networkidle")
        await asyncio.sleep(3)
        
        # Enable Real APIs for slower, more visible execution
        print("✅ Enabling Real APIs checkbox...")
        try:
            api_checkbox = page.locator('input[type="checkbox"]').first
            if not await api_checkbox.is_checked():
                await api_checkbox.click()
                await asyncio.sleep(1)
                print("   ✓ Real APIs enabled")
        except:
            print("   ⚠️ Could not find API checkbox (might be in demo mode)")
        
        # Submit a complex query that should take time
        complex_query = "Research the history of electric vehicles and find our company's policy on vehicle reimbursement"
        
        print(f"\n📝 Submitting complex query: '{complex_query}'")
        chat_input = page.locator('textarea[data-testid="stChatInputTextArea"]')
        await chat_input.fill(complex_query)
        await chat_input.press("Enter")
        
        print("\n👀 WATCHING FOR REAL-TIME UPDATES (next 15 seconds):")
        print("=" * 70)
        
        # Monitor for 15 seconds, checking every 0.5 seconds
        start_time = time.time()
        last_status = {}
        update_count = 0
        
        for i in range(30):  # 30 checks over 15 seconds
            elapsed = time.time() - start_time
            
            # Look for the Live Agent Status section in the last assistant message
            try:
                # Get all agent status lines
                coordinator = await page.locator('text=/Coordinator:.*$/').last.text_content(timeout=1000)
                research = await page.locator('text=/Research:.*$/').last.text_content(timeout=1000)
                document = await page.locator('text=/Document:.*$/').last.text_content(timeout=1000)
                summarizer = await page.locator('text=/Summarizer:.*$/').last.text_content(timeout=1000)
                
                current_status = {
                    'coordinator': coordinator,
                    'research': research,
                    'document': document,
                    'summarizer': summarizer
                }
                
                # Check if status changed
                if current_status != last_status and last_status:
                    update_count += 1
                    print(f"\n[{elapsed:.1f}s] 🔄 STATUS UPDATE #{update_count}:")
                    for agent, status in current_status.items():
                        if status != last_status.get(agent):
                            print(f"   {agent}: {last_status.get(agent, 'N/A')} → {status}")
                
                last_status = current_status
                
            except Exception as e:
                if i == 0:
                    print(f"[{elapsed:.1f}s] ⏳ Waiting for status to appear...")
            
            await asyncio.sleep(0.5)
        
        print("\n" + "=" * 70)
        print(f"\n📊 TEST RESULTS:")
        print(f"   Total updates detected: {update_count}")
        print(f"\n   Final Status:")
        for agent, status in last_status.items():
            print(f"      {agent}: {status}")
        
        if update_count >= 4:
            print("\n   ✅ SUCCESS: Detected multiple real-time updates during execution!")
        elif update_count > 0:
            print("\n   ⚠️  PARTIAL: Some updates detected, but may not be truly real-time")
        else:
            print("\n   ❌ FAILED: No status updates detected during execution")
            print("      Agents may be completing too fast or updates not streaming")
        
        print("\n📸 Taking final screenshot...")
        await page.screenshot(path="c:/Users/segayle/repos/lo/week3/realtime_test.png", full_page=True)
        print("   Saved to: week3/realtime_test.png")
        
        # Keep browser open for manual inspection
        print("\n👁️  Browser will stay open for 10 seconds for manual verification...")
        await asyncio.sleep(10)
        
        await browser.close()
        print("\n✨ Test complete!")

if __name__ == "__main__":
    asyncio.run(test_realtime_updates())
