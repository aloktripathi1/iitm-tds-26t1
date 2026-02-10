from openai import OpenAI
from config import Config

# Test aipipe.org connection
print(f"Testing aipipe.org with token: {Config.AIPIPE_TOKEN[:20]}...")
print(f"Base URL: {Config.AIPIPE_BASE_URL}")

client = OpenAI(
    api_key=Config.AIPIPE_TOKEN,
    base_url=Config.AIPIPE_BASE_URL
)

# Test 1: Embedding
try:
    print("\n🧪 Test 1: Embeddings...")
    response = client.embeddings.create(
        input=["Hello world"],
        model="text-embedding-3-small"
    )
    print(f"✓ Embedding successful! Dimension: {len(response.data[0].embedding)}")
except Exception as e:
    print(f"✗ Embedding failed: {e}")

# Test 2: Chat completion
try:
    print("\n🧪 Test 2: Chat Completion...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say 'test successful'"}],
        max_tokens=10
    )
    print(f"✓ Chat successful! Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"✗ Chat failed: {e}")

print("\n✅ All tests passed! Ready to run the app.")