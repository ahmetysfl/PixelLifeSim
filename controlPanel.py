import pygame
from settings import BUTTON_TEXTS, INFO_TEXTS, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_MARGIN, BUTTON_FONT_SIZE, INFO_FONT_SIZE, BUTTON_TEXT_COLOR, PAUSE_BUTTON_COLOR, STOP_BUTTON_COLOR, DIVIDER_LINE_COLOR, INFO_TEXT_COLOR

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

        # Seçilen yaratığın bilgileri
        self.selected_creature_info = None

        # Courier New yazı tipi (bold olarak ayarlandı)
        self.monospace_font = pygame.font.SysFont("couriernew", INFO_FONT_SIZE, bold=True)

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

    # Yaratığa tıklanıp tıklanmadığını kontrol et
    def check_creature_click(self, mouse_pos, creatures):
        """
        Fare tıklamasının bir yaratığa denk gelip gelmediğini kontrol eder.

        :param mouse_pos: Fare imlecinin konumu (x, y).
        :param creatures: Yaratık listesi.
        :return: Tıklanan yaratık varsa onu döndürür, yoksa None.
        """
        for creature in creatures:
            creature_rect = pygame.Rect(creature.x, creature.y, creature.creature_size, creature.creature_size)
            if creature_rect.collidepoint(mouse_pos):
                return creature
        return None

    # Bilgi metnini çiz
    def draw_info_text(self, screen, text, x, y):
        """
        Bilgi metnini ekrana çizer.

        :param screen: Pygame ekran yüzeyi.
        :param text: Çizilecek metin.
        :param x: Metnin x koordinatı.
        :param y: Metnin y koordinatı.
        """
        text_surface = self.monospace_font.render(text, True, INFO_TEXT_COLOR)
        screen.blit(text_surface, (x, y))

    # Kontrol panelini çiz
    # controlPanel.py

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
        pause_button_text = BUTTON_TEXTS["resume"] if self.paused else BUTTON_TEXTS["pause"]
        self.draw_button(screen, pause_button_text, self.pause_button_rect, PAUSE_BUTTON_COLOR)
        self.draw_button(screen, BUTTON_TEXTS["stop"], self.stop_button_rect, STOP_BUTTON_COLOR)

        # Seçilen yaratığın genetics bilgilerini göster
        if self.selected_creature_info:
            genetics = self.selected_creature_info.genetics
            info_texts = [
                INFO_TEXTS["consumption_rate"].format(genetics.consumption_rate),
                INFO_TEXTS["action_zone_ratio"].format(genetics.action_zone_ratio),
                INFO_TEXTS["production_rate"].format(genetics.production_rate),
                INFO_TEXTS["energy_capacity"].format(genetics.energy_capacity),
                INFO_TEXTS["consume_others"].format(genetics.consume_other_creatures_ratio),
                INFO_TEXTS["resource_share"].format(genetics.resource_share_ratio),
                INFO_TEXTS["sense_radius"].format(genetics.sense_radius)  # Yeni eklenen değer
            ]
            # Bilgileri durdur butonunun altına yaz
            y_offset = self.stop_button_rect.bottom + BUTTON_MARGIN
            for text in info_texts:
                self.draw_info_text(screen, text, self.screen_width + BUTTON_MARGIN, y_offset)
                y_offset += INFO_FONT_SIZE + 5  # Satırlar arası boşluk (INFO_FONT_SIZE kullanılıyor)

    # Olayları işle
    def handle_events(self, event, creatures):
        """
        Pygame olaylarını işler.

        :param event: Pygame olayı.
        :param creatures: Yaratık listesi.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.is_button_clicked(mouse_pos, self.pause_button_rect):
                self.paused = not self.paused  # Duraklatma durumunu tersine çevir
            elif self.is_button_clicked(mouse_pos, self.stop_button_rect):
                self.stopped = True  # Simülasyonu durdur
            elif self.paused:  # Oyun durmuşken yaratığa tıklanırsa
                clicked_creature = self.check_creature_click(mouse_pos, creatures)
                if clicked_creature:
                    self.selected_creature_info = clicked_creature
