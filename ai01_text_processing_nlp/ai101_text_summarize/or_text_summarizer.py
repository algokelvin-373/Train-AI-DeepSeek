import requests
import json

"""
    Fungsi untuk meringkas teks menggunakan OpenRouter API

    Parameters:
    - text: Teks yang akan diringkas
    - api_key: API key OpenRouter Anda
    - model: Model yang digunakan (default: deepseek/deepseek-r1:free)
    - max_length: Panjang maksimal ringkasan (dalam tokens/karakter)
    """
def summarize_text(text, api_key, model="deepseek/deepseek-r1:free", max_length=1000):
    system_prompt = """Anda adalah asisten yang ahli dalam meringkas teks. 
    Buatlah ringkasan yang padat, informatif, dan mudah dipahami dari teks yang diberikan.
    Pertahankan poin-poin penting dan inti dari teks asli."""

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"Tolong ringkas teks berikut:\n\n{text}\n\nRingkasan:"
                    }
                ],
                "max_tokens": max_length,
                "temperature": 0.3,
            })
        )

        if response.status_code == 200:
            result = response.json()
            summary = result['choices'][0]['message']['content']
            return summary.strip()
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

def main():
    API_KEY = "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"

    # Example text
    sample_text = """
        Artificial Intelligence (AI) adalah cabang ilmu komputer yang berfokus pada 
        pembuatan mesin yang dapat melakukan tugas-tugas yang biasanya membutuhkan 
        kecerdasan manusia. AI mencakup berbagai teknologi seperti machine learning, 
        natural language processing, computer vision, dan robotics. 

        Perkembangan AI telah membawa revolusi dalam banyak bidang, termasuk 
        kesehatan, pendidikan, transportasi, dan bisnis. Mesin dapat belajar dari 
        data, mengenali pola, membuat keputusan, dan bahkan berinteraksi dengan 
        manusia secara alami. 

        Namun, perkembangan AI juga menimbulkan tantangan etis dan sosial, 
        seperti masalah privasi, bias algoritma, dan dampaknya terhadap lapangan kerja. 
        Penting untuk mengembangkan AI yang bertanggung jawab dan bermanfaat bagi 
        seluruh umat manusia.
        """

    print("Text Original:")
    print(sample_text)
    print(len(sample_text))
    print("\n" + "=" * 50 + "\n")

    # Call function summarizer
    summary = summarize_text(sample_text, API_KEY)
    if summary:
        print("Ringkasan:")
        print(summary)
    else:
        print("Gagal membuat ringkasan")


if __name__ == "__main__":
    main()
    print("\n" + "=" * 80 + "\n")