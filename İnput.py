import streamlit as st
import math
import google.generativeai as genai
from collections import Counter
import random
from PIL import Image 
import io 

st.set_page_config(layout="wide")

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except KeyError:
    st.error("Google API anahtarı bulunamadı. Lütfen '.streamlit/secrets.toml' dosyasında 'GOOGLE_API_KEY' anahtarınızı tanımlayın.")
    API_KEY = None

if API_KEY:
    model_for_qa = genai.GenerativeModel('gemini-2.0-flash')
    model_for_generation = genai.GenerativeModel('gemini-2.0-flash') 

st.title("Matematiksel İşlemler Uygulaması")
st.write("Lütfen soldaki menüden ünite seçin ve ardından işlem yapmak istediğiniz konuyu seçin.")

# --- Sidebar (Kenar Çubuğu) ---
st.sidebar.title("Üniteler")
unit_choice = st.sidebar.radio(
    "Lütfen bir ünite seçin:",
    ("Ünite 3", "Ünite 6", "Soru İste", "Soru Çözümü") # Yeni radio butonu eklendi
)

# --- Ana İçerik Alanı ---
if unit_choice == "Ünite 3":
    st.header("3. Ünite: Temel Matematiksel İşlemler")

    tab1, tab2, tab3, tab4 = st.tabs(["Köklü Sayılar", "Mutlak Değer", "Üslü Sayılar", "Çarpanlara Ayırma"])

    with tab1: # Köklü Sayılar Sekmesi
        st.subheader("Köklü Sayılar")
        sayi_kok = st.number_input("Karekökünü almak istediğiniz sayıyı girin:", value=0.0, format="%.2f", key="kok_sayi")
        if st.button("Karekök Hesapla", key="kok_button"):
            if sayi_kok >= 0:
                sonuc_kok = math.sqrt(sayi_kok)
                st.success(f"√{sayi_kok} = **{sonuc_kok}**")
            else:
                st.error("Negatif sayıların karekökü reel bir sayı değildir.")
        st.info("Karekök işlemi sadece pozitif veya sıfır sayılar için reel sonuç verir.")

    with tab2: # Mutlak Değer Sekmesi
        st.subheader("Mutlak Değer")
        sayi_mutlak = st.number_input("Mutlak değerini almak istediğiniz sayıyı girin:", value=0.0, format="%.2f", key="mutlak_sayi")
        if st.button("Mutlak Değer Hesapla", key="mutlak_button"):
            sonuc_mutlak = abs(sayi_mutlak)
            st.success(f"|{sayi_mutlak}| = **{sonuc_mutlak}**")

    with tab3: # Üslü Sayılar Sekmesi
        st.subheader("Üslü Sayılar")
        taban = st.number_input("Taban sayıyı girin:", value=0.0, format="%.2f", key="taban_sayi")
        kuvvet = st.number_input("Üssü girin:", value=0.0, format="%.2f", key="kuvvet_sayi")
        if st.button("Üslü Sayı Hesapla", key="uslu_button"):
            try:
                sonuc_uslu = taban ** kuvvet
                st.success(f"{taban}^{kuvvet} = **{sonuc_uslu}**")
            except OverflowError:
                st.error("Sayı çok büyük, hesaplanamıyor. Daha küçük sayılar deneyin.")
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")

    with tab4: # Çarpanlara Ayırma Sekmesi
        st.subheader("Çarpanlara Ayırma")
        st.write("Bu bölümde sayıların çarpanlarına ayrılması işlemleri yapılacaktır.")
        
        number_to_factor = st.number_input("Çarpanlarına ayırmak istediğiniz pozitif tam sayıyı girin (en fazla 1.000.000):", min_value=1, max_value=1000000, value=1, step=1, key="factor_num")
        
        def get_factors(n):
            factors = []
            for i in range(1, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    factors.append(i)
                    if i * i != n:
                        factors.append(n // i)
            factors.sort()
            return factors

        if st.button("Çarpanlara Ayır", key="factor_button"):
            if number_to_factor > 0 and isinstance(number_to_factor, int):
                factors = get_factors(int(number_to_factor))
                if len(factors) == 2 and factors[0] == 1 and factors[1] == number_to_factor:
                    st.success(f"**{int(number_to_factor)}** bir asal sayıdır. Çarpanları: {factors}")
                else:
                    st.success(f"**{int(number_to_factor)}** sayısının çarpanları: {factors}")
            else:
                st.error("Lütfen pozitif bir tam sayı girin.")

elif unit_choice == "Ünite 6":
    st.header("6. Ünite: Olasılık ve Sayma")

    tab1, tab2, tab3 = st.tabs(["Permütasyon", "Kombinasyon", "Tekrarlı Permütasyon"])

    with tab1: # Permütasyon Sekmesi
        st.subheader("Permütasyon (nPr)")
        n_p = st.number_input("Toplam eleman sayısı (n):", min_value=0, step=1, value=0, key="n_p")
        r_p = st.number_input("Seçilen eleman sayısı (r):", min_value=0, step=1, value=0, key="r_p")
        
        def factorial(k):
            if k == 0: return 1
            return math.factorial(k)

        if st.button("Permütasyon Hesapla", key="perm_button"):
            if n_p >= r_p:
                try:
                    result_p = factorial(n_p) / factorial(n_p - r_p)
                    st.success(f"P({n_p}, {r_p}) = **{int(result_p)}**")
                except OverflowError:
                    st.error("Sayılar çok büyük, hesaplanamıyor.")
            else:
                st.error("n, r'den küçük olamaz. (n >= r olmalı)")

    with tab2: # Kombinasyon Sekmesi
        st.subheader("Kombinasyon (nCr)")
        n_c = st.number_input("Toplam eleman sayısı (n):", min_value=0, step=1, value=0, key="n_c")
        r_c = st.number_input("Seçilen eleman sayısı (r):", min_value=0, step=1, value=0, key="r_c")

        def nCr(n, r):
            if r < 0 or r > n: return 0
            if r == 0 or r == n: return 1
            if r > n // 2: r = n - r
            return factorial(n) // (factorial(r) * factorial(n - r))

        if st.button("Kombinasyon Hesapla", key="comb_button"):
            if n_c >= r_c:
                try:
                    result_c = nCr(int(n_c), int(r_c))
                    st.success(f"C({n_c}, {r_c}) = **{int(result_c)}**")
                except OverflowError:
                    st.error("Sayılar çok büyük, hesaplanamıyor.")
            else:
                st.error("n, r'den küçük olamaz. (n >= r olmalı)")

    with tab3: # Tekrarlı Permütasyon Sekmesi
        st.subheader("Tekrarlı Permütasyon")
        st.write("Formül: n! / (n1! * n2! * ... * nk!)")
        st.write("Örnek: 'AAB' kelimesindeki permütasyon sayısı (3! / (2! * 1!))")
        
        text_input = st.text_input("Harfleri girin (ör: AABAC):", key="repeated_perm_text")
        
        def repeated_permutations(s):
            n = len(s)
            counts = Counter(s)
            
            denominator = 1
            for count in counts.values():
                denominator *= factorial(count)
            
            if denominator == 0: return 0
            
            try:
                return factorial(n) // denominator
            except OverflowError:
                return "Sayı çok büyük"

        if st.button("Tekrarlı Permütasyon Hesapla", key="repeated_perm_button"):
            if text_input:
                result_rp = repeated_permutations(text_input.strip())
                st.success(f"'{text_input}' kelimesinin tekrarlı permütasyon sayısı: **{result_rp}**")
            else:
                st.warning("Lütfen harfleri girin.")

# --- "Soru İste" Ünitesi ---
elif unit_choice == "Soru İste":
    st.header("Rastgele Matematik Sorusu")
    st.write("Aşağıdaki alana istediğiniz matematik konusunu (örneğin: 'limitler', 'türev', 'integraller', 'olasılık') yazın ve size o konuda bir soru üreteyim.")

    if not API_KEY:
        st.warning("Google API anahtarı bulunamadığı için soru üretilemiyor. Lütfen '.streamlit/secrets.toml' dosyasında 'GOOGLE_API_KEY' anahtarınızı tanımlayın.")
    else:
        konu = st.text_input("Matematik konusu girin (Türkçe veya İngilizce):", key="mat_konu")
        zorluk_seviyesi = st.selectbox(
            "Zorluk seviyesi seçin:",
            ("Başlangıç", "Orta", "İleri"),
            key="zorluk_seviyesi"
        )
        
        # Bu bölümdeki session state'ler sadece "Soru İste" için olsun
        # "Soru Çözümü" için ayrı session state'ler kullanacağız
        if 'gen_current_question' not in st.session_state: st.session_state.gen_current_question = None
        if 'gen_current_answer' not in st.session_state: st.session_state.gen_current_answer = None
        if 'gen_current_solution' not in st.session_state: st.session_state.gen_current_solution = None
        if 'gen_show_answer' not in st.session_state: st.session_state.gen_show_answer = False
        if 'gen_show_solution' not in st.session_state: st.session_state.gen_show_solution = False
        if 'gen_show_question_again' not in st.session_state: st.session_state.gen_show_question_again = False


        if st.button("Soru Üret", key="generate_question_button"):
            if konu:
                # Durumları sıfırla
                st.session_state.gen_show_answer = False
                st.session_state.gen_show_solution = False
                st.session_state.gen_show_question_again = False
                st.session_state.gen_current_question = None
                st.session_state.gen_current_answer = None
                st.session_state.gen_current_solution = None

                # Prompt'u güncelledik: Kesinlik ve tutarlılık vurgusu eklendi
                system_instruction_prefix_gen = """Sen bir uzman matematik öğretmenisin. Üniversiteye hazırlanan bir öğrenciye eksiksiz ve doğru bilgi sağlayacaksın. Bana sadece bir matematik problem sorusu, sorunun **kesinlikle doğru** olan cevabı ve adım adım **tamamıyla doğru ve tutarlı** çözümünü ayrı ayrı belirtir misin? Çözüm ve cevap birbiriyle **mutlaka uyumlu** olmalı. Başka hiçbir açıklama, yorum veya ek bilgi yapma.
                Format şöyle olsun:
                Soru: [soru metni]
                Cevap: [cevap metni]
                Çözüm: [çözüm metni]"""
                
                prompt_text_for_gemini_gen = f"{system_instruction_prefix_gen}\nKonu: '{konu}', Zorluk: '{zorluk_seviyesi}'."
                
                with st.spinner("Sorunuz, cevabı ve çözümü üretiliyor..."):
                    try:
                        response = model_for_generation.generate_content(prompt_text_for_gemini_gen)
                        
                        response_text = response.text.strip()
                        # Yanıtı parse etme (Soru, Cevap, Çözüm)
                        if "Soru:" in response_text and "Cevap:" in response_text and "Çözüm:" in response_text:
                            question_part = response_text.split("Soru:")[1].split("Cevap:")[0].strip()
                            answer_part = response_text.split("Cevap:")[1].split("Çözüm:")[0].strip()
                            solution_part = response_text.split("Çözüm:")[1].strip()

                            st.session_state.gen_current_question = question_part
                            st.session_state.gen_current_answer = answer_part
                            st.session_state.gen_current_solution = solution_part
                            
                            st.subheader("Üretilen Sorunuz:")
                            st.markdown(f"**{st.session_state.gen_current_question}**")
                            st.session_state.gen_show_answer = False
                            st.session_state.gen_show_solution = False
                            st.session_state.gen_show_question_again = True
                        else:
                            st.error("Modelden beklenen formatta bir yanıt alınamadı (Soru, Cevap, Çözüm bekleniyor). Lütfen tekrar deneyin.")
                            st.error(f"Model yanıtı (hata ayıklama için): {response_text}")
                            st.session_state.gen_current_question = None
                            st.session_state.gen_current_answer = None
                            st.session_state.gen_current_solution = None
                            st.session_state.gen_show_question_again = False
                            st.session_state.gen_show_answer = False
                            st.session_state.gen_show_solution = False

                    except Exception as e:
                        st.error(f"Soru üretilirken bir hata oluştu: {e}")
                        st.session_state.gen_current_question = None
                        st.session_state.gen_current_answer = None
                        st.session_state.gen_current_solution = None
                        st.session_state.gen_show_question_again = False
                        st.session_state.gen_show_answer = False
                        st.session_state.gen_show_solution = False
            else:
                st.warning("Lütfen bir matematik konusu girin.")
        
        # Butonları yan yana yerleştirmek için sütunlar kullanıldı
        col1_gen, col2_gen, col3_gen = st.columns(3)

        if st.session_state.gen_current_question: # Sadece soru varsa butonları göster
            with col1_gen:
                if st.button("Cevabı Göster/Gizle", key="gen_toggle_answer_button"):
                    st.session_state.gen_show_answer = not st.session_state.gen_show_answer
                    st.session_state.gen_show_solution = False # Cevabı gösterirken çözümü gizle
            
            with col2_gen:
                if st.session_state.gen_show_question_again:
                    if st.button("Soruyu Tekrar Göster", key="gen_show_question_again_button"):
                        st.session_state.gen_show_answer = False
                        st.session_state.gen_show_solution = False
                        st.subheader("Üretilen Sorunuz:")
                        st.markdown(f"**{st.session_state.gen_current_question}**")
            
            with col3_gen:
                if st.session_state.gen_current_solution:
                    if st.button("Çözümü Anlat", key="gen_show_solution_button"):
                        st.session_state.gen_show_solution = not st.session_state.gen_show_solution
                        st.session_state.gen_show_answer = False # Çözümü gösterirken cevabı gizle

            # Gösterilecek bilgileri yönet
            if st.session_state.gen_show_answer:
                st.subheader("Üretilen Cevap:")
                st.info(st.session_state.gen_current_answer)
            elif st.session_state.gen_show_solution:
                st.subheader("Üretilen Çözüm:")
                st.success(st.session_state.gen_current_solution)
            elif st.session_state.gen_current_question and not (st.session_state.gen_show_answer or st.session_state.gen_show_solution):
                st.info("Cevabı görmek için 'Cevabı Göster/Gizle', çözümü görmek için 'Çözümü Anlat' butonuna tıklayın.")

# --- Yeni "Soru Çözümü" Ünitesi ---
elif unit_choice == "Soru Çözümü":
    st.header("Kendi Sorunuzu Çözün")
    st.write("Aşağıdaki alana matematik sorunuzu yazın veya bir görsel yükleyin. Yapay zeka size cevap ve çözüm sunacaktır.")

    if not API_KEY:
        st.warning("Google API anahtarı bulunamadığı için soru çözümü yapılamıyor. Lütfen '.streamlit/secrets.toml' dosyasında 'GOOGLE_API_KEY' anahtarınızı tanımlayın.")
    else:
        # Oturum durumu değişkenleri (çözüm için)
        if 'solve_current_answer' not in st.session_state: st.session_state.solve_current_answer = None
        if 'solve_current_solution' not in st.session_state: st.session_state.solve_current_solution = None
        if 'solve_show_answer' not in st.session_state: st.session_state.solve_show_answer = False
        if 'solve_show_solution' not in st.session_state: st.session_state.solve_show_solution = False
        if 'uploaded_image_data' not in st.session_state: st.session_state.uploaded_image_data = None
        if 'current_uploaded_image_display' not in st.session_state: st.session_state.current_uploaded_image_display = None


        question_input_type = st.radio(
            "Sorunuzu nasıl girmek istersiniz?",
            ("Metin Olarak Yaz", "Görsel Yükle"),
            key="question_input_type"
        )

        user_question_text = ""
        uploaded_file = None
        
        # Yüklenen görselin gösterimi için placeholder
        image_placeholder = st.empty()

        if question_input_type == "Metin Olarak Yaz":
            user_question_text = st.text_area("Lütfen matematik sorunuzu buraya yazın:", height=150, key="user_question_text")
            st.session_state.uploaded_image_data = None # Metin seçiliyse görseli sıfırla
            st.session_state.current_uploaded_image_display = None # Görsel gösterimini sıfırla
        else: # Görsel Yükle
            uploaded_file = st.file_uploader("Lütfen bir resim dosyası yükleyin (.jpg, .jpeg, .png):", type=["jpg", "jpeg", "png"], key="image_uploader")
            
            if uploaded_file is not None:
                # Dosya yüklenirse yeni görseli işle
                image = Image.open(uploaded_file)
                             
                if image.mode == 'RGBA':
                    image_to_save = image # PNG RGBA'yı destekler
                elif image.mode == 'P': # Paletli moddaysa RGB'ye dönüştür
                    image_to_save = image.convert('RGB')
                else:
                    image_to_save = image.convert('RGB') 

                img_byte_arr = io.BytesIO()
                # Modu kontrol edip doğru formatta kaydet
                if image_to_save.mode == 'RGBA':
                    image_to_save.save(img_byte_arr, format='PNG')
                else:
                    image_to_save.save(img_byte_arr, format='JPEG')

                image_data = img_byte_arr.getvalue()
                
                st.session_state.uploaded_image_data = image_data 
                st.session_state.current_uploaded_image_display = image 
            
            # Yüklenmiş görseli göster (hem yeni yükleneni hem de session state'teki)
            if st.session_state.current_uploaded_image_display is not None:
                image_placeholder.image(st.session_state.current_uploaded_image_display, caption='Yüklenen Soru Görseli', width=300)


        if st.button("Soruyu Çöz", key="solve_question_button"):
            # Her çözme denemesinde durumu sıfırla
            st.session_state.solve_show_answer = False
            st.session_state.solve_show_solution = False
            st.session_state.solve_current_answer = None
            st.session_state.solve_current_solution = None

            content_parts = []
            valid_input = False

            if question_input_type == "Metin Olarak Yaz" and user_question_text:
                content_parts.append(user_question_text)
                valid_input = True
            elif question_input_type == "Görsel Yükle" and st.session_state.uploaded_image_data:
                try:
                    # Saklanan byte verisinden PIL Image nesnesini yeniden oluştur
                    image_from_bytes = Image.open(io.BytesIO(st.session_state.uploaded_image_data))
                    content_parts.append(image_from_bytes)
                    valid_input = True
                except Exception as e:
                    st.error(f"Saklanan görsel işlenirken bir hata oluştu: {e}")
                    valid_input = False
            
            if not valid_input:
                st.warning("Lütfen bir soru metni girin veya bir görsel yükleyin.")
            elif not API_KEY:
                st.warning("API anahtarı bulunamadığı için işlem yapılamaz.")
            else:
                prompt_for_solve = """Sen bir uzman matematik öğretmenisin. Sana verilen matematik sorusunu dikkatlice incele. Soruyu **kesinlikle doğru** bir şekilde çöz ve cevabı ile adım adım **tamamıyla doğru ve tutarlı** çözümünü ayrı ayrı belirt. Çözüm ve cevap birbiriyle **mutlaka uyumlu** olmalı. Başka hiçbir açıklama, yorum veya ek bilgi yapma.
                Format şöyle olsun:
                Cevap: [cevap metni]
                Çözüm: [çözüm metni]"""
                
                # Modelin içeriğini oluştur
                full_content = [prompt_for_solve] + content_parts
                
                with st.spinner("Sorunuz çözülüyor..."):
                    try:
                        # Model_for_qa'yı kullanarak generate_content çağrısı yapıyoruz
                        response = model_for_qa.generate_content(full_content)
                        
                        response_text = response.text.strip()
                        if "Cevap:" in response_text and "Çözüm:" in response_text:
                            answer_part = response_text.split("Cevap:")[1].split("Çözüm:")[0].strip()
                            solution_part = response_text.split("Çözüm:")[1].strip()

                            st.session_state.solve_current_answer = answer_part
                            st.session_state.solve_current_solution = solution_part
                            
                            st.success("Çözüm başarıyla oluşturuldu!")
                        else:
                            st.error("Modelden beklenen formatta bir yanıt alınamadı (Cevap ve Çözüm bekleniyor). Lütfen tekrar deneyin veya daha net bir soru girin.")
                            st.error(f"Model yanıtı (hata ayıklama için): {response_text}")
                            st.session_state.solve_current_answer = None
                            st.session_state.solve_current_solution = None

                    except Exception as e:
                        st.error(f"Soruyu çözerken bir hata oluştu: {e}")
                        st.session_state.solve_current_answer = None
                        st.session_state.solve_current_solution = None

        # Çözüm ve Cevap butonları
        col1_solve, col2_solve = st.columns(2)

        if st.session_state.solve_current_answer or st.session_state.solve_current_solution:
            with col1_solve:
                if st.button("Cevabı Göster/Gizle", key="solve_toggle_answer_button"):
                    st.session_state.solve_show_answer = not st.session_state.solve_show_answer
                    st.session_state.solve_show_solution = False # Cevabı gösterirken çözümü gizle
            
            with col2_solve:
                if st.session_state.solve_current_solution:
                    if st.button("Çözümü Anlat", key="solve_show_solution_button"):
                        st.session_state.solve_show_solution = not st.session_state.solve_show_solution
                        st.session_state.solve_show_answer = False # Çözümü gösterirken cevabı gizla
            
            # Gösterilecek bilgileri yönet
            if st.session_state.solve_show_answer:
                st.subheader("Sorunuzun Cevabı:")
                st.info(st.session_state.solve_current_answer)
            elif st.session_state.solve_show_solution:
                st.subheader("Sorunuzun Çözümü:")
                st.success(st.session_state.solve_current_solution)
            elif (st.session_state.solve_current_answer or st.session_state.solve_current_solution) and not (st.session_state.solve_show_answer or st.session_state.solve_show_solution):
                st.info("Cevabı görmek için 'Cevabı Göster/Gizle', çözümü görmek için 'Çözümü Anlat' butonuna tıklayın.")

st.markdown("---")
st.write("Desingn By Ege Özdemir")
