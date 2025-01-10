import pygame

# Global ayarlar
BUTTON_WIDTH = 100  # Butonların genişliği
BUTTON_HEIGHT = 50  # Butonların yüksekliği
BUTTON_MARGIN = 20  # Butonlar arasındaki boşluk
BUTTON_FONT_SIZE = 24  # Buton yazılarının font boyutu (24 olarak güncellendi)
BUTTON_TEXT_COLOR = (255, 255, 255)  # Buton yazılarının rengi (beyaz)
PAUSE_BUTTON_COLOR = (0, 128, 255)  # Duraklat butonunun rengi (mavi)
STOP_BUTTON_COLOR = (255, 0, 0)  # Durdur butonunun rengi (kırmızı)
DIVIDER_LINE_COLOR = (255, 255, 255)  # Ayırıcı çizginin rengi (beyaz)

class ControlPanel:
    def __init__(self, screen_width, screen_height):
        """
        Kontrol paneli sınıfı.

        :param screen_width: Simülasyon ekranının genişliği.
        :param screen_height: Simülasyon ekranının yüksekliği.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Butonların konum ve boyutları
        self.pause_button_rect = pygame.Rect(
            screen_width + BUTTON_MARGIN,  # X konumu
            BUTTON_MARGIN,                 # Y konumu
            BUTTON_WIDTH,                  # Genişlik
            BUTTON_HEIGHT                  # Yükseklik
        )
        self.stop_button_rect = pygame.Rect(
            screen_width + BUTTON_MARGIN,  # X konumu
            BUTTON_MARGIN * 2 + BUTTON_HEIGHT,  # Y konumu (pause butonunun altında)
            BUTTON_WIDTH,                  # Genişlik
            BUTTON_HEIGHT                  # Yükseklik
        )

        # Duraklatma ve durdurma durumları
        self.paused = False
        self.stopped = False

    # Buton çizme fonksiyonu
    def draw_button(self, screen, text, rect, color):
        """
        Buton çizer.

        :param screen: Pygame ekran yüzeyi.
        :param text: Buton üzerinde görünecek metin.
        :param rect: Butonun konum ve boyut bilgileri (pygame.Rect).
        :param color: Butonun rengi.
        """
        pygame.draw.rect(screen, color, rect)
        font = pygame.font.Font(None, BUTTON_FONT_SIZE)
        text_surface = font.render(text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    # Buton tıklama kontrolü
    def is_button_clicked(self, mouse_pos, button_rect):
        """
        Butonun tıklanıp tıklanmadığını kontrol eder.

        :param mouse_pos: Fare imlecinin konumu (x, y).
        :param button_rect: Butonun konum ve boyut bilgileri (pygame.Rect).
        :return: Buton tıklanmışsa True, aksi takdirde False.
        """
        return button_rect.collidepoint(mouse_pos)

    # Kontrol panelini çiz
    def draw(self, screen):
        """
        Kontrol panelini ekrana çizer.

        :param screen: Pygame ekran yüzeyi.
        """
        # Simülasyon ekranı ile kontrol paneli arasına beyaz çizgi çiz
        pygame.draw.line(
            screen,
            DIVIDER_LINE_COLOR,
            (self.screen_width, 0),  # Çizginin başlangıç noktası
            (self.screen_width, self.screen_height),  # Çizginin bitiş noktası
            2  # Çizgi kalınlığı
        )

        # Duraklat butonunun metnini oyunun durumuna göre değiştir
        pause_button_text = "Devam Et" if self.paused else "Duraklat"
        self.draw_button(screen, pause_button_text, self.pause_button_rect, PAUSE_BUTTON_COLOR)
        self.draw_button(screen, "Durdur", self.stop_button_rect, STOP_BUTTON_COLOR)

    # Olayları işle
    def handle_events(self, event):
        """
        Pygame olaylarını işler.

        :param event: Pygame olayı.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.is_button_clicked(mouse_pos, self.pause_button_rect):
                self.paused = not self.paused  # Duraklatma durumunu tersine çevir
            elif self.is_button_clicked(mouse_pos, self.stop_button_rect):
                self.stopped = True  # Simülasyonu durdur
