#!/usr/bin/env python3
"""Generate file://-compatible translated UI and stage data.

Run python3 pipeline/build_i18n.py after editing this file or competition_stages.json.
Every locale owns every string; placeholders are validated before writing.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES = {'en': 'en-US', 'fr': 'fr-FR', 'ru': 'ru-RU', 'tr': 'tr-TR', 'pl': 'pl-PL', 'es': 'es-ES', 'pt': 'pt-PT', 'de': 'de-DE', 'ko': 'ko-KR', 'zh': 'zh-CN'}
NAMES = {'en': 'English', 'fr': 'Français', 'ru': 'Русский', 'tr': 'Türkçe', 'pl': 'Polski', 'es': 'Español', 'pt': 'Português', 'de': 'Deutsch', 'ko': '한국어', 'zh': '简体中文'}

# Shared label translations follow the sister Capitol site.
T = {
  "en": {
    "overview": "Overview",
    "members": "Members",
    "opponent": "Opponent",
    "trends": "Trends",
    "data": "Data",
    "language": "Language",
    "skip": "Skip to content",
    "copy_link": "Copy link",
    "copied": "Link copied",
    "theme_light": "Switch to day mode",
    "theme_dark": "Switch to night mode",
    "points": "Points",
    "rank": "Rank",
    "tier": "Tier",
    "active_only": "Active players only",
    "change": "vs previous",
    "download_csv": "Download CSV",
    "close": "Close",
    "no_results": "No matches",
    "depth": "Points by rank tier",
    "expand": "Chart and table",
    "difference": "Difference",
    "total": "Total points",
    "methodology": "How the data is collected"
  },
  "fr": {
    "overview": "Aperçu",
    "members": "Membres",
    "opponent": "Adversaire",
    "trends": "Tendances",
    "data": "Données",
    "language": "Langue",
    "skip": "Aller au contenu",
    "copy_link": "Copier le lien",
    "copied": "Lien copié",
    "theme_light": "Passer en mode jour",
    "theme_dark": "Passer en mode nuit",
    "points": "Points",
    "rank": "Rang",
    "tier": "Tranche",
    "active_only": "Joueurs actifs uniquement",
    "change": "vs précédent",
    "download_csv": "Télécharger le CSV",
    "close": "Fermer",
    "no_results": "Aucun résultat",
    "depth": "Points par tranche de rang",
    "expand": "Graphique et tableau",
    "difference": "Écart",
    "total": "Points totaux",
    "methodology": "Comment les données sont collectées"
  },
  "ru": {
    "overview": "Обзор",
    "members": "Участники",
    "opponent": "Противник",
    "trends": "Динамика",
    "data": "Данные",
    "language": "Язык",
    "skip": "Перейти к содержимому",
    "copy_link": "Копировать ссылку",
    "copied": "Ссылка скопирована",
    "theme_light": "Дневной режим",
    "theme_dark": "Ночной режим",
    "points": "Очки",
    "rank": "Место",
    "tier": "Группа",
    "active_only": "Только активные игроки",
    "change": "к прошлому",
    "download_csv": "Скачать CSV",
    "close": "Закрыть",
    "no_results": "Ничего не найдено",
    "depth": "Очки по группам мест",
    "expand": "График и таблица",
    "difference": "Разница",
    "total": "Всего очков",
    "methodology": "Как собираются данные"
  },
  "tr": {
    "overview": "Genel bakış",
    "members": "Üyeler",
    "opponent": "Rakip",
    "trends": "Eğilimler",
    "data": "Veri",
    "language": "Dil",
    "skip": "İçeriğe geç",
    "copy_link": "Bağlantıyı kopyala",
    "copied": "Bağlantı kopyalandı",
    "theme_light": "Gündüz moduna geç",
    "theme_dark": "Gece moduna geç",
    "points": "Puan",
    "rank": "Sıra",
    "tier": "Dilim",
    "active_only": "Yalnızca aktif oyuncular",
    "change": "Öncekine göre",
    "download_csv": "CSV indir",
    "close": "Kapat",
    "no_results": "Sonuç yok",
    "depth": "Sıra dilimine göre puan",
    "expand": "Grafik ve tablo",
    "difference": "Fark",
    "total": "Toplam puan",
    "methodology": "Veriler nasıl toplanır"
  },
  "pl": {
    "overview": "Przegląd",
    "members": "Członkowie",
    "opponent": "Przeciwnik",
    "trends": "Trendy",
    "data": "Dane",
    "language": "Język",
    "skip": "Przejdź do treści",
    "copy_link": "Kopiuj link",
    "copied": "Skopiowano link",
    "theme_light": "Tryb dzienny",
    "theme_dark": "Tryb nocny",
    "points": "Punkty",
    "rank": "Miejsce",
    "tier": "Przedział",
    "active_only": "Tylko aktywni gracze",
    "change": "vs poprzednie",
    "download_csv": "Pobierz CSV",
    "close": "Zamknij",
    "no_results": "Brak wyników",
    "depth": "Punkty według przedziałów miejsc",
    "expand": "Wykres i tabela",
    "difference": "Różnica",
    "total": "Łączne punkty",
    "methodology": "Jak zbierane są dane"
  },
  "es": {
    "overview": "Resumen",
    "members": "Miembros",
    "opponent": "Rival",
    "trends": "Tendencias",
    "data": "Datos",
    "language": "Idioma",
    "skip": "Saltar al contenido",
    "copy_link": "Copiar enlace",
    "copied": "Enlace copiado",
    "theme_light": "Cambiar a modo día",
    "theme_dark": "Cambiar a modo noche",
    "points": "Puntos",
    "rank": "Puesto",
    "tier": "Tramo",
    "active_only": "Solo jugadores activos",
    "change": "vs anterior",
    "download_csv": "Descargar CSV",
    "close": "Cerrar",
    "no_results": "Sin resultados",
    "depth": "Puntos por tramo de puesto",
    "expand": "Gráfico y tabla",
    "difference": "Diferencia",
    "total": "Puntos totales",
    "methodology": "Cómo se recopilan los datos"
  },
  "pt": {
    "overview": "Visão geral",
    "members": "Membros",
    "opponent": "Adversário",
    "trends": "Tendências",
    "data": "Dados",
    "language": "Idioma",
    "skip": "Saltar para o conteúdo",
    "copy_link": "Copiar ligação",
    "copied": "Ligação copiada",
    "theme_light": "Mudar para modo dia",
    "theme_dark": "Mudar para modo noite",
    "points": "Pontos",
    "rank": "Posição",
    "tier": "Escalão",
    "active_only": "Apenas jogadores ativos",
    "change": "vs anterior",
    "download_csv": "Transferir CSV",
    "close": "Fechar",
    "no_results": "Sem resultados",
    "depth": "Pontos por escalão de posição",
    "expand": "Gráfico e tabela",
    "difference": "Diferença",
    "total": "Pontos totais",
    "methodology": "Como os dados são recolhidos"
  },
  "de": {
    "overview": "Übersicht",
    "members": "Mitglieder",
    "opponent": "Gegner",
    "trends": "Trends",
    "data": "Daten",
    "language": "Sprache",
    "skip": "Zum Inhalt springen",
    "copy_link": "Link kopieren",
    "copied": "Link kopiert",
    "theme_light": "Tagmodus",
    "theme_dark": "Nachtmodus",
    "points": "Punkte",
    "rank": "Rang",
    "tier": "Stufe",
    "active_only": "Nur aktive Spieler",
    "change": "ggü. vorher",
    "download_csv": "CSV herunterladen",
    "close": "Schließen",
    "no_results": "Keine Treffer",
    "depth": "Punkte nach Rangstufe",
    "expand": "Diagramm und Tabelle",
    "difference": "Differenz",
    "total": "Punkte gesamt",
    "methodology": "So werden die Daten erhoben"
  },
  "ko": {
    "overview": "개요",
    "members": "인원",
    "opponent": "상대",
    "trends": "추세",
    "data": "데이터",
    "language": "언어",
    "skip": "본문으로 건너뛰기",
    "copy_link": "링크 복사",
    "copied": "링크 복사됨",
    "theme_light": "주간 모드로 전환",
    "theme_dark": "야간 모드로 전환",
    "points": "포인트",
    "rank": "순위",
    "tier": "구간",
    "active_only": "활성 플레이어만",
    "change": "이전 대비",
    "download_csv": "CSV 다운로드",
    "close": "닫기",
    "no_results": "결과 없음",
    "depth": "순위 구간별 포인트",
    "expand": "차트와 표",
    "difference": "차이",
    "total": "총 포인트",
    "methodology": "데이터 수집 방법"
  },
  "zh": {
    "overview": "概览",
    "members": "成员",
    "opponent": "对手",
    "trends": "趋势",
    "data": "数据",
    "language": "语言",
    "skip": "跳到主要内容",
    "copy_link": "复制链接",
    "copied": "链接已复制",
    "theme_light": "切换到日间模式",
    "theme_dark": "切换到夜间模式",
    "points": "积分",
    "rank": "排名",
    "tier": "区间",
    "active_only": "仅显示活跃玩家",
    "change": "对比上次",
    "download_csv": "下载 CSV",
    "close": "关闭",
    "no_results": "无匹配结果",
    "depth": "按排名区间的积分",
    "expand": "图表和表格",
    "difference": "差值",
    "total": "总积分",
    "methodology": "数据收集方式"
  }
}

# Columns: key | English | French | Russian | Turkish | Polish | Spanish |
# Portuguese | German | Korean | Simplified Chinese. No fallback strings.
TRANSLATIONS = r"""
leaderboards|Leaderboards|Classements|Рейтинги|Sıralamalar|Rankingi|Clasificaciones|Classificações|Ranglisten|순위표|排行榜
stages|Stages|Étapes|Этапы|Aşamalar|Etapy|Etapas|Etapas|Etappen|단계|阶段
week|Week|Semaine|Неделя|Hafta|Tydzień|Semana|Semana|Woche|주|周
search|Search players|Rechercher des joueurs|Поиск игроков|Oyuncu ara|Szukaj graczy|Buscar jugadores|Procurar jogadores|Spieler suchen|플레이어 검색|搜索玩家
loading|Loading…|Chargement…|Загрузка…|Yükleniyor…|Ładowanie…|Cargando…|A carregar…|Wird geladen…|불러오는 중…|加载中…
error|Could not load this week.|Impossible de charger cette semaine.|Не удалось загрузить эту неделю.|Bu hafta yüklenemedi.|Nie udało się wczytać tego tygodnia.|No se pudo cargar esta semana.|Não foi possível carregar esta semana.|Diese Woche konnte nicht geladen werden.|이번 주를 불러올 수 없습니다.|无法加载本周数据。
retry|Try again|Réessayer|Повторить|Tekrar dene|Spróbuj ponownie|Reintentar|Tentar novamente|Erneut versuchen|다시 시도|重试
final|Final|Définitif|Завершён|Tamamlandı|Zakończony|Finalizado|Final|Abgeschlossen|확정|已结束
live|Live|En cours|В процессе|Canlı|Na żywo|En curso|Em curso|Laufend|진행 중|实时
pending|Not started|Non commencé|Не начат|Başlamadı|Nie rozpoczęto|Sin empezar|Por iniciar|Noch nicht begonnen|시작 전|未开始
leading|Leading|En tête|Лидирует|Önde|Prowadzi|En cabeza|Na frente|In Führung|우세|领先
trailing|Trailing|Derrière|Отстаёт|Geride|Przegrywa|Por detrás|Atrás|Im Rückstand|열세|落后
clinched|{name} clinched|{name} a assuré la victoire|{name} обеспечил победу|{name} galibiyeti garantiledi|{name} zapewnia sobie zwycięstwo|{name} aseguró la victoria|{name} garantiu a vitória|{name} hat den Sieg gesichert|{name} 승리 확정|{name} 已锁定胜利
in_progress|In progress|En cours|В процессе|Devam ediyor|W toku|En curso|Em curso|Läuft|진행 중|进行中
captured|Captured {date}|Capturé le {date}|Снято {date}|Kayıt: {date}|Zapisano {date}|Capturado el {date}|Capturado em {date}|Erfasst am {date}|캡처: {date}|采集于 {date}
weekly_points|Weekly points|Points hebdomadaires|Очки за неделю|Haftalık puan|Punkty tygodniowe|Puntos semanales|Pontos semanais|Wochenpunkte|주간 포인트|周积分
share|Share|Part|Доля|Pay|Udział|Proporción|Quota|Anteil|비중|占比
quota|Quota|Objectif|Норма|Hedef|Cel|Objetivo|Meta|Soll|목표|配额
met|Met|Atteint|Выполнена|Ulaşıldı|Osiągnięty|Alcanzado|Atingida|Erfüllt|달성|已达标
near|Near|Proche|Близко|Yakın|Blisko|Cerca|Perto|Fast erreicht|근접|接近
below|Below|En dessous|Ниже нормы|Altında|Poniżej|Por debajo|Abaixo|Darunter|미달|未达标
deficit|Deficit|Manque|Нехватка|Eksik|Brak|Déficit|Défice|Fehlbetrag|부족분|差额
players|Players|Joueurs|Игроки|Oyuncular|Gracze|Jugadores|Jogadores|Spieler|플레이어|玩家
player|Player|Joueur|Игрок|Oyuncu|Gracz|Jugador|Jogador|Spieler|플레이어|玩家
active_days|Active days|Jours actifs|Активные дни|Aktif günler|Aktywne dni|Días activos|Dias ativos|Aktive Tage|활동 일수|活跃天数
consistency|Consistency|Régularité|Стабильность|İstikrar|Regularność|Regularidad|Regularidade|Beständigkeit|꾸준함|稳定性
checksum|Checksum|Vérification des totaux|Проверка суммы|Toplam kontrolü|Kontrola sumy|Comprobación de sumas|Verificação de somas|Summenprüfung|합계 검증|合计校验
exact|Exact|Conforme|Совпадает|Tam eşleşme|Zgodna|Exacto|Exato|Exakt|일치|一致
alliance_change|Alliance change|Changement d'alliance|Смена альянса|İttifak değişikliği|Zmiana sojuszu|Cambio de alianza|Mudança de aliança|Allianzwechsel|연맹 변경|联盟变更
mismatch|Mismatch|Écart|Расхождение|Uyuşmazlık|Rozbieżność|Discrepancia|Divergência|Abweichung|불일치|不一致
all|All|Tous|Все|Tümü|Wszyscy|Todos|Todos|Alle|전체|全部
filter|Filter|Filtrer|Фильтр|Filtre|Filtruj|Filtrar|Filtrar|Filtern|필터|筛选
sort|Sort|Trier|Сортировка|Sırala|Sortuj|Ordenar|Ordenar|Sortieren|정렬|排序
days|Days|Jours|Дни|Günler|Dni|Días|Dias|Tage|일수|天数
mon|Mon|Lun|Пн|Pzt|Pon|Lun|Seg|Mo|월|周一
tue|Tue|Mar|Вт|Sal|Wt|Mar|Ter|Di|화|周二
wed|Wed|Mer|Ср|Çar|Śr|Mié|Qua|Mi|수|周三
thu|Thu|Jeu|Чт|Per|Czw|Jue|Qui|Do|목|周四
fri|Fri|Ven|Пт|Cum|Pt|Vie|Sex|Fr|금|周五
sat|Sat|Sam|Сб|Cmt|Sob|Sáb|Sáb|Sa|토|周六
week_board|This Week|Cette semaine|Эта неделя|Bu hafta|Ten tydzień|Esta semana|Esta semana|Diese Woche|이번 주|本周
download_json|Download JSON|Télécharger le JSON|Скачать JSON|JSON indir|Pobierz JSON|Descargar JSON|Transferir JSON|JSON herunterladen|JSON 다운로드|下载 JSON
live_note|Live snapshot: points and ranks may change.|Instantané en cours : les points et les rangs peuvent changer.|Текущий снимок: очки и места могут измениться.|Canlı kayıt: puanlar ve sıralamalar değişebilir.|Migawka na żywo: punkty i miejsca mogą się zmienić.|Captura en curso: los puntos y puestos pueden cambiar.|Captura em curso: os pontos e as posições podem mudar.|Laufende Momentaufnahme: Punkte und Ränge können sich ändern.|진행 중인 기록입니다. 포인트와 순위가 바뀔 수 있습니다.|实时快照：积分与排名可能变化。
stage_points|Points per stage|Points par étape|Очки по этапам|Aşama başına puan|Punkty na etap|Puntos por etapa|Pontos por etapa|Punkte je Etappe|단계별 포인트|各阶段积分
rest|Rest|Reste|Остальные|Diğerleri|Pozostali|Resto|Restantes|Übrige|나머지|其余
head_to_head|Head-to-head by rank|Duel par rang|Сравнение по месту|Sıraya göre karşılaştırma|Porównanie według miejsca|Cara a cara por puesto|Frente a frente por posição|Direktvergleich nach Rang|순위별 맞대결|同排名对比
top_performers|Top performers|Meilleurs joueurs|Лучшие игроки|En iyi oyuncular|Najlepsi gracze|Mejores jugadores|Melhores jogadores|Beste Spieler|최고 성적 플레이어|最佳玩家
record|Record|Bilan|Результат|Galibiyet–mağlubiyet|Bilans|Balance|Balanço|Bilanz|전적|战绩
stage_win_rate|Stage win rate|Taux de victoire par étape|Доля побед по этапам|Aşama kazanma oranı|Odsetek wygranych etapów|Porcentaje de victorias por etapa|Taxa de vitórias por etapa|Siegquote je Etappe|단계별 승률|各阶段胜率
career|Member career|Parcours des membres|История участников|Üye geçmişi|Historia członków|Trayectoria de miembros|Percurso dos membros|Mitgliederverlauf|멤버 누적 기록|成员历程
weeks_played|Weeks played|Semaines jouées|Недель сыграно|Katıldığı haftalar|Rozegrane tygodnie|Semanas jugadas|Semanas jogadas|Gespielte Wochen|참가 주 수|参赛周数
average|Average|Moyenne|Среднее|Ortalama|Średnia|Promedio|Média|Durchschnitt|평균|平均
best|Best|Meilleur|Лучший|En iyi|Najlepszy|Mejor|Melhor|Beste|최고|最佳
last_week|Last week|Dernière semaine|Последняя неделя|Son hafta|Ostatni tydzień|Última semana|Última semana|Letzte Woche|마지막 주|最近一周
trend|Trend|Tendance|Динамика|Eğilim|Trend|Tendencia|Tendência|Entwicklung|추세|趋势
need_two|Trends need at least two recorded weeks.|Les tendances nécessitent au moins deux semaines enregistrées.|Для динамики нужны хотя бы две записанные недели.|Eğilimler için en az iki haftalık kayıt gerekir.|Trendy wymagają co najmniej dwóch zapisanych tygodni.|Las tendencias requieren al menos dos semanas registradas.|As tendências precisam de pelo menos duas semanas registadas.|Trends erfordern mindestens zwei erfasste Wochen.|추세를 보려면 최소 두 주의 기록이 필요합니다.|至少记录两周后才可显示趋势。
history|Weekly history|Historique hebdomadaire|История по неделям|Haftalık geçmiş|Historia tygodniowa|Historial semanal|Histórico semanal|Wochenverlauf|주간 기록|每周历史
best_week|Best week|Meilleure semaine|Лучшая неделя|En iyi hafta|Najlepszy tydzień|Mejor semana|Melhor semana|Beste Woche|최고 기록 주|最佳周
daily_ranks|Daily ranks|Rangs quotidiens|Места по дням|Günlük sıralamalar|Dzienne miejsca|Puestos diarios|Posições diárias|Tagesränge|일별 순위|每日排名
overall_rank|Overall rank|Rang général|Общее место|Genel sıra|Miejsce ogólne|Puesto general|Posição geral|Gesamtrang|전체 순위|总排名
alliance_rank|Alliance rank|Rang dans l'alliance|Место в альянсе|İttifak sırası|Miejsce w sojuszu|Puesto en la alianza|Posição na aliança|Allianzrang|연맹 내 순위|联盟内排名
integrity|Data integrity|Intégrité des données|Целостность данных|Veri bütünlüğü|Integralność danych|Integridad de datos|Integridade dos dados|Datenintegrität|데이터 무결성|数据完整性
rows|Rows|Lignes|Строки|Satırlar|Wiersze|Filas|Linhas|Zeilen|행 수|行数
contiguous|Contiguous ranks|Rangs consécutifs|Без пропусков мест|Kesintisiz sıralar|Ciągłość miejsc|Puestos consecutivos|Posições consecutivas|Lückenlose Ränge|연속 순위|排名连续
descending|Points descending|Points décroissants|Очки по убыванию|Azalan puanlar|Punkty malejąco|Puntos descendentes|Pontos decrescentes|Punkte absteigend|포인트 내림차순|积分降序
unresolved|Unresolved|Non résolu|Не разрешено|Çözümlenmemiş|Nierozstrzygnięte|Sin resolver|Por resolver|Ungeklärt|미해결|未解决
yes|Yes|Oui|Да|Evet|Tak|Sí|Sim|Ja|예|是
no|No|Non|Нет|Hayır|Nie|No|Não|Nein|아니요|否
screenshots|Capture screenshots|Captures d'écran|Снимки экрана|Ekran görüntüleri|Zrzuty ekranu|Capturas de pantalla|Capturas de ecrã|Bildschirmaufnahmen|캡처 화면|采集截图
methodology_text|Captured from the game client using on-device text recognition. Every rank is read at least twice and voted; gaps are re-read. Live tabs are scanned twice and merged.|Capturé depuis le client du jeu par reconnaissance de texte sur l'appareil. Chaque rang est lu au moins deux fois et retenu par vote ; les lacunes sont relues. Les onglets en cours sont parcourus deux fois puis fusionnés.|Данные снимаются с игрового клиента и распознаются на устройстве. Каждое место читается не менее двух раз и выбирается голосованием; пропуски читаются повторно. Текущие вкладки сканируются дважды и объединяются.|Oyun istemcisinden cihaz üzerinde metin tanımayla kaydedilir. Her sıra en az iki kez okunup oylamayla belirlenir; boşluklar yeniden okunur. Canlı sekmeler iki kez taranıp birleştirilir.|Dane są zapisywane z klienta gry i odczytywane przez rozpoznawanie tekstu na urządzeniu. Każde miejsce jest odczytywane co najmniej dwukrotnie i wybierane głosowaniem; luki są odczytywane ponownie. Karty na żywo są skanowane dwukrotnie i scalane.|Se captura desde el cliente del juego mediante reconocimiento de texto en el dispositivo. Cada puesto se lee al menos dos veces y se decide por votación; los huecos se releen. Las pestañas en curso se escanean dos veces y se combinan.|Capturado do cliente do jogo com reconhecimento de texto no dispositivo. Cada posição é lida pelo menos duas vezes e escolhida por votação; as lacunas são relidas. Os separadores em curso são lidos duas vezes e combinados.|Aus dem Spielclient mit Texterkennung auf dem Gerät erfasst. Jeder Rang wird mindestens zweimal gelesen und per Abstimmung gewählt; Lücken werden erneut gelesen. Laufende Reiter werden zweimal erfasst und zusammengeführt.|게임 클라이언트 화면을 기기 내 문자 인식으로 읽습니다. 모든 순위를 최소 두 번 읽고 다수결로 결정하며, 누락 부분은 다시 읽습니다. 진행 중인 탭은 두 번 스캔하여 병합합니다.|从游戏客户端采集，并使用设备端文字识别。每个名次至少读取两次并通过投票确定；缺漏处重新读取。实时标签页扫描两次后合并。
server_time|Server time (UTC−2)|Heure serveur (UTC−2)|Время сервера (UTC−2)|Sunucu saati (UTC−2)|Czas serwera (UTC−2)|Hora del servidor (UTC−2)|Hora do servidor (UTC−2)|Serverzeit (UTC−2)|서버 시간 (UTC−2)|服务器时间（UTC−2）
rules|Rules|Règles|Правила|Kurallar|Zasady|Reglas|Regras|Regeln|규칙|规则
rules_text|Monday awards 1 win, Tuesday–Friday 2 each, and Saturday 4: 13 total. Seven wins clinch the match. Only final stages count toward the score.|Le lundi rapporte 1 victoire, du mardi au vendredi 2 chacune, et le samedi 4 : 13 au total. Sept victoires assurent le match. Seules les étapes terminées comptent dans le score.|Понедельник даёт 1 победу, вторник–пятница по 2, суббота 4: всего 13. Семь побед гарантируют выигрыш матча. В счёт входят только завершённые этапы.|Pazartesi 1, salı–cuma günde 2, cumartesi 4 galibiyet verir: toplam 13. Yedi galibiyet maçı kazanmayı garantiler. Skora yalnızca tamamlanan aşamalar sayılır.|Poniedziałek daje 1 wygraną, wtorek–piątek po 2, a sobota 4: łącznie 13. Siedem wygranych zapewnia zwycięstwo w meczu. Do wyniku liczą się tylko zakończone etapy.|El lunes otorga 1 victoria, de martes a viernes 2 cada día y el sábado 4: 13 en total. Siete victorias aseguran el duelo. Solo las etapas finalizadas cuentan en el marcador.|Segunda-feira dá 1 vitória, terça a sexta 2 por dia e sábado 4: 13 no total. Sete vitórias garantem o duelo. Só as etapas concluídas contam para o resultado.|Montag zählt 1 Sieg, Dienstag–Freitag je 2 und Samstag 4: insgesamt 13. Sieben Siege sichern den Gesamtsieg. Nur abgeschlossene Etappen zählen zum Spielstand.|월요일은 1승, 화요일~금요일은 하루 2승, 토요일은 4승으로 총 13승입니다. 7승을 확보하면 승리가 확정됩니다. 완료된 단계만 점수에 반영됩니다.|周一计1胜，周二至周五每天计2胜，周六计4胜，共13胜。获得7胜即可锁定胜利。比分仅计入已结束的阶段。
footer|Z Route: Redemption · Server 117 · VS intelligence · maintained by JeffxLabs|Z Route: Redemption · Serveur 117 · Renseignement VS · maintenu par JeffxLabs|Z Route: Redemption · Сервер 117 · Аналитика VS · поддерживает JeffxLabs|Z Route: Redemption · Sunucu 117 · VS analizleri · JeffxLabs tarafından hazırlanır|Z Route: Redemption · Serwer 117 · Analiza VS · prowadzi JeffxLabs|Z Route: Redemption · Servidor 117 · Análisis VS · mantenido por JeffxLabs|Z Route: Redemption · Servidor 117 · Análise VS · mantido por JeffxLabs|Z Route: Redemption · Server 117 · VS-Analyse · betreut von JeffxLabs|Z Route: Redemption · 서버 117 · VS 분석 · 운영: JeffxLabs|Z Route: Redemption · 服务器117 · VS情报 · 由JeffxLabs维护
titan|Titan|Titan|Титан|Dev|Tytan|Titán|Titã|Titan|거인|巨擘
high|High scorer|Gros contributeur|Высокий вклад|Yüksek puanlı|Wysoki wynik|Gran contribuidor|Grande contribuidor|Hohe Punktzahl|고득점|高分
core|Core|Noyau|Основа|Çekirdek|Trzon|Núcleo|Núcleo|Kern|핵심|核心
quota_met|Quota met|Objectif atteint|Норма выполнена|Hedefe ulaştı|Cel osiągnięty|Objetivo alcanzado|Meta atingida|Soll erfüllt|목표 달성|配额达标
near_quota|Near quota|Proche de l'objectif|Близко к норме|Hedefe yakın|Blisko celu|Cerca del objetivo|Perto da meta|Nahe am Soll|목표 근접|接近配额
passenger|Passenger|Passager|Пассажир|Yolcu|Pasażer|Pasajero|Passageiro|Mitläufer|저참여|低贡献
check_exact|Daily sum matches weekly points.|La somme des jours correspond aux points hebdomadaires.|Сумма дней совпадает с очками за неделю.|Günlük toplam haftalık puanla eşleşiyor.|Suma dni zgadza się z punktami tygodniowymi.|La suma diaria coincide con los puntos semanales.|A soma diária corresponde aos pontos semanais.|Die Tagessumme entspricht den Wochenpunkten.|일별 합계와 주간 포인트가 일치합니다.|每日合计与周积分一致。
check_live|Live capture: daily and weekly totals may differ.|Capture en cours : les totaux quotidiens et hebdomadaires peuvent différer.|Текущий снимок: дневная сумма и очки за неделю могут отличаться.|Canlı kayıt: günlük ve haftalık toplamlar farklı olabilir.|Zapis na żywo: suma dni i punkty tygodniowe mogą się różnić.|Captura en curso: los totales diarios y semanales pueden diferir.|Captura em curso: os totais diários e semanais podem diferir.|Laufende Erfassung: Tages- und Wochensummen können abweichen.|진행 중인 캡처로 일별 합계와 주간 합계가 다를 수 있습니다.|实时采集：每日合计与周合计可能不同。
check_alliance_change|Alliance membership changed during this week.|L'appartenance à l'alliance a changé durant cette semaine.|Принадлежность к альянсу изменилась на этой неделе.|Bu hafta ittifak üyeliği değişti.|Przynależność do sojuszu zmieniła się w tym tygodniu.|La pertenencia a la alianza cambió durante esta semana.|A pertença à aliança mudou durante esta semana.|Die Allianzzugehörigkeit hat sich in dieser Woche geändert.|이번 주에 소속 연맹이 변경되었습니다.|本周内联盟归属发生变化。
check_mismatch|Daily sum differs from weekly points; review capture data.|La somme des jours diffère des points hebdomadaires ; vérifier les captures.|Сумма дней отличается от очков за неделю; проверьте снимки.|Günlük toplam haftalık puandan farklı; kayıt verilerini inceleyin.|Suma dni różni się od punktów tygodniowych; sprawdź dane zrzutów.|La suma diaria difiere de los puntos semanales; revise las capturas.|A soma diária difere dos pontos semanais; consulte as capturas.|Die Tagessumme weicht von den Wochenpunkten ab; Aufnahmen prüfen.|일별 합계와 주간 포인트가 다릅니다. 캡처 데이터를 확인하세요.|每日合计与周积分不符，请查看采集数据。
match|Match|Duel|Матч|Maç|Mecz|Duelo|Duelo|Duell|대결|对决
score|{home} : {opp} / {total}|{home} : {opp} / {total}|{home} : {opp} / {total}|{home} : {opp} / {total}|{home} : {opp} / {total}|{home} : {opp} / {total}|{home} : {opp} / {total}|{home} : {opp} / {total}|{home} : {opp} / {total}|{home} : {opp} / {total}
wins_remaining|{n} wins remaining|{n} victoires restantes|Осталось побед: {n}|Kalan galibiyet: {n}|Pozostałe wygrane: {n}|Quedan {n} victorias|Restam {n} vitórias|{n} Siege verbleiben|남은 승수: {n}|剩余 {n} 胜
top10|Top 10|10 premiers|Топ-10|İlk 10|Najlepsza 10|Primeros 10|Primeiros 10|Beste 10|상위 10명|前10名
top20|Ranks 11–20|Rangs 11–20|Места 11–20|11–20. sıralar|Miejsca 11–20|Puestos 11–20|Posições 11–20|Ränge 11–20|11~20위|第11至20名
top50|Ranks 21–50|Rangs 21–50|Места 21–50|21–50. sıralar|Miejsca 21–50|Puestos 21–50|Posições 21–50|Ränge 21–50|21~50위|第21至50名
top100|Ranks 51–100|Rangs 51–100|Места 51–100|51–100. sıralar|Miejsca 51–100|Puestos 51–100|Posições 51–100|Ränge 51–100|51~100위|第51至100名
wins_one|{n} win|{n} victoire|{n} победа|{n} galibiyet|{n} wygrana|{n} victoria|{n} vitória|{n} Sieg|{n}승|{n}胜
wins_other|{n} wins|{n} victoires|{n} победы|{n} galibiyet|{n} wygranej|{n} victorias|{n} vitórias|{n} Siege|{n}승|{n}胜
wins_few|{n} wins|{n} victoires|{n} победы|{n} galibiyet|{n} wygrane|{n} victorias|{n} vitórias|{n} Siege|{n}승|{n}胜
wins_many|{n} wins|{n} victoires|{n} побед|{n} galibiyet|{n} wygranych|{n} victorias|{n} vitórias|{n} Siege|{n}승|{n}胜
joined|Joined|A rejoint|Присоединился|Katıldı|Dołączył|Se incorporó|Entrou|Beigetreten|가입|已加入
left|Left|A quitté|Покинул|Ayrıldı|Odszedł|Se fue|Saiu|Ausgetreten|탈퇴|已离开
include_left|Include players who left|Inclure les joueurs partis|Включить ушедших игроков|Ayrılan oyuncuları dahil et|Uwzględnij graczy, którzy odeszli|Incluir jugadores que se fueron|Incluir jogadores que saíram|Ausgetretene Spieler einbeziehen|탈퇴한 플레이어 포함|包括已离开的玩家
check_joined|First appeared on a daily board after Monday; points earned before joining appear only in the weekly total.|Première apparition sur un classement quotidien après lundi ; les points gagnés avant de rejoindre figurent uniquement dans le total hebdomadaire.|Впервые появился в дневном рейтинге после понедельника; очки до вступления учтены только в недельном итоге.|Pazartesiden sonra ilk kez günlük sıralamada göründü; katılmadan önce kazanılan puanlar yalnızca haftalık toplamda yer alır.|Po raz pierwszy pojawił się w rankingu dziennym po poniedziałku; punkty zdobyte przed dołączeniem są tylko w sumie tygodniowej.|Apareció por primera vez en una clasificación diaria después del lunes; los puntos anteriores a su incorporación solo figuran en el total semanal.|Apareceu pela primeira vez numa classificação diária após segunda-feira; os pontos anteriores à entrada constam apenas do total semanal.|Erschien erstmals nach Montag auf einer Tagesrangliste; Punkte vor dem Beitritt sind nur in der Wochensumme enthalten.|월요일 이후 일일 순위표에 처음 등장했습니다. 가입 전 획득한 포인트는 주간 합계에만 포함됩니다.|周一后首次出现在每日榜单上；加入前获得的积分仅计入周合计。
check_left|Appears on daily boards but is no longer on the weekly board; excluded from weekly ranks.|Figure sur des classements quotidiens mais plus sur le classement hebdomadaire ; exclu des rangs hebdomadaires.|Есть в дневных рейтингах, но больше нет в недельном; не участвует в недельном ранжировании.|Günlük sıralamalarda var ancak artık haftalık sıralamada yok; haftalık derecelendirmeye dahil edilmez.|Jest w rankingach dziennych, ale nie ma go już w tygodniowym; nie otrzymuje pozycji tygodniowej.|Figura en clasificaciones diarias, pero ya no en la semanal; no recibe puesto semanal.|Consta de classificações diárias, mas já não da semanal; não recebe posição semanal.|Auf Tagesranglisten, aber nicht mehr auf der Wochenrangliste; ohne Wochenplatzierung.|일일 순위표에는 있지만 주간 순위표에는 더 이상 없습니다. 주간 순위에서 제외됩니다.|出现在每日榜单上，但已不在周榜单中；不参与周排名。
win|Win|Victoire|Победа|Galibiyet|Wygrana|Victoria|Vitória|Sieg|승|胜
loss|Loss|Défaite|Поражение|Mağlubiyet|Przegrana|Derrota|Derrota|Niederlage|패|负
undecided|Undecided|Non décidé|Не решён|Sonuçlanmadı|Nierozstrzygnięty|Sin decidir|Por decidir|Offen|미확정|未决
not_on_weekly|Not on weekly board|Absent du classement hebdomadaire|Нет в недельном рейтинге|Haftalık sıralamada yok|Brak w rankingu tygodniowym|No figura en la tabla semanal|Ausente da tabela semanal|Nicht in der Wochenrangliste|주간 순위표에 없음|未上周榜
copy_manual|Copy this link|Copier ce lien|Скопируйте эту ссылку|Bu bağlantıyı kopyala|Skopiuj ten link|Copiar este enlace|Copiar esta ligação|Diesen Link kopieren|이 링크 복사|复制此链接
quota_target|Weekly target: {n}|Objectif hebdomadaire : {n}|Норма за неделю: {n}|Haftalık hedef: {n}|Cel tygodniowy: {n}|Objetivo semanal: {n}|Meta semanal: {n}|Wochenziel: {n}|주간 목표: {n}|周目标：{n}
rank_change_note|Rank change compares with the previous day's full board.|La variation de rang compare avec le classement complet du jour précédent.|Изменение места сравнивается с полной таблицей предыдущего дня.|Sıra değişimi önceki günün tam sıralamasıyla karşılaştırılır.|Zmiana miejsca jest liczona względem pełnego rankingu poprzedniego dnia.|El cambio de puesto se compara con la tabla completa del día anterior.|A variação de posição compara com a tabela completa do dia anterior.|Rangänderungen beziehen sich auf die vollständige Rangliste des Vortags.|순위 변화는 전날 전체 순위표와 비교합니다.|排名变化与前一天的完整排行榜比较。
capture_note|Only completed stages count toward the match score; live leads are provisional.|Seules les étapes terminées comptent dans le score ; les avances en cours sont provisoires.|В счёт входят только завершённые этапы; текущее лидерство предварительное.|Maç skoruna yalnızca tamamlanan aşamalar sayılır; canlı liderlik geçicidir.|Do wyniku meczu liczą się tylko zakończone etapy; prowadzenie na żywo jest tymczasowe.|Solo las etapas completadas cuentan en el marcador; las ventajas en curso son provisionales.|Só as etapas concluídas contam para o resultado; as vantagens em curso são provisórias.|Nur abgeschlossene Etappen zählen zum Spielstand; laufende Führungen sind vorläufig.|완료된 단계만 대결 점수에 반영하며 진행 중인 우세는 잠정적입니다.|比分仅计入已结束阶段，实时领先结果尚未确定。
stage_1|Radar Exploration|Exploration radar|Радарная разведка|Radar keşfi|Eksploracja radarowa|Exploración de radar|Exploração de radar|Radarerkundung|레이더 탐색|雷达探索
stage_2|Base Construction|Construction de base|Строительство базы|Üs inşası|Budowa bazy|Construcción de base|Construção da base|Basisausbau|기지 건설|基地建设
stage_3|Tech Research|Recherche technologique|Исследование технологий|Teknoloji araştırması|Badania technologiczne|Investigación tecnológica|Investigação tecnológica|Technologieforschung|기술 연구|科技研究
stage_4|Hero Training|Entraînement des héros|Подготовка героев|Kahraman eğitimi|Szkolenie bohaterów|Entrenamiento de héroes|Treino de heróis|Heldentraining|영웅 훈련|英雄训练
stage_5|Full Military Preparation|Préparation militaire complète|Полная военная подготовка|Tam askerî hazırlık|Pełne przygotowanie wojskowe|Preparación militar completa|Preparação militar completa|Umfassende Militärvorbereitung|전면 군사 준비|全面军事准备
stage_6|Enemy Assault|Assaut ennemi|Штурм противника|Düşmana saldırı|Szturm na wroga|Asalto al enemigo|Assalto ao inimigo|Feindangriff|적 공격|突袭敌军
stage_desc_1|Exploration, radar tasks, fighter development, stamina use and resource gathering.|Exploration, missions radar, développement des chasseurs, dépense d'endurance et collecte de ressources.|Разведка, задания радара, развитие истребителя, расход выносливости и сбор ресурсов.|Keşif, radar görevleri, savaşçı geliştirme, dayanıklılık kullanımı ve kaynak toplama.|Eksploracja, zadania radarowe, rozwój myśliwca, zużycie wytrzymałości i zbieranie zasobów.|Exploración, misiones de radar, desarrollo del caza, uso de energía y recolección de recursos.|Exploração, tarefas de radar, desenvolvimento do caça, uso de resistência e recolha de recursos.|Erkundung, Radaraufgaben, Jägerentwicklung, Ausdauerverbrauch und Ressourcensammlung.|탐색, 레이더 임무, 전투기 개발, 스태미나 사용 및 자원 채집.|探索、雷达任务、战斗机发展、体力消耗和资源采集。
stage_desc_2|Base expansion, construction power, building speedups, survivor recruitment and UR logistics.|Extension de base, puissance de construction, accélérations de construction, recrutement de survivants et logistique UR.|Расширение базы, сила строительства, ускорения строительства, набор выживших и логистика UR.|Üs genişletme, inşaat gücü, inşaat hızlandırmaları, hayatta kalan alımı ve UR lojistiği.|Rozbudowa bazy, moc budowy, przyspieszenia budowy, rekrutacja ocalałych i logistyka UR.|Ampliación de base, poder de construcción, aceleraciones de construcción, reclutamiento de supervivientes y logística UR.|Expansão da base, poder de construção, acelerações de construção, recrutamento de sobreviventes e logística UR.|Basisausbau, Baumacht, Baubeschleunigungen, Überlebendenrekrutierung und UR-Logistik.|기지 확장, 건설 전투력, 건설 가속, 생존자 모집 및 UR 물류.|基地扩建、建设战力、建造加速、幸存者招募及UR物流。
stage_desc_3|Technology, research speedups, research power and fighter component chests.|Technologie, accélérations de recherche, puissance de recherche et coffres de composants de chasseurs.|Технологии, ускорения исследований, сила исследований и сундуки компонентов истребителя.|Teknoloji, araştırma hızlandırmaları, araştırma gücü ve savaşçı bileşen sandıkları.|Technologia, przyspieszenia badań, moc badań i skrzynie komponentów myśliwca.|Tecnología, aceleraciones de investigación, poder de investigación y cofres de componentes del caza.|Tecnologia, acelerações de investigação, poder de investigação e baús de componentes do caça.|Technologie, Forschungsbeschleunigungen, Forschungsmacht und Jägerkomponententruhen.|기술, 연구 가속, 연구 전투력 및 전투기 부품 상자.|科技、研究加速、研究战力及战斗机组件宝箱。
stage_desc_4|Hero development and recruitment, skill EXP books, hero EXP and UR/SSR/SR hero shards.|Développement et recrutement des héros, livres d'EXP de compétence, EXP de héros et fragments de héros UR/SSR/SR.|Развитие и набор героев, книги опыта навыков, опыт героев и фрагменты героев UR/SSR/SR.|Kahraman geliştirme ve alımı, beceri deneyim kitapları, kahraman deneyimi ve UR/SSR/SR kahraman parçaları.|Rozwój i rekrutacja bohaterów, księgi doświadczenia umiejętności, doświadczenie bohaterów i fragmenty bohaterów UR/SSR/SR.|Desarrollo y reclutamiento de héroes, libros de experiencia de habilidades, experiencia de héroes y fragmentos de héroes UR/SSR/SR.|Desenvolvimento e recrutamento de heróis, livros de experiência de habilidades, experiência de heróis e fragmentos de heróis UR/SSR/SR.|Heldenentwicklung und -rekrutierung, Fertigkeits-EP-Bücher, Helden-EP und UR/SSR/SR-Heldensplitter.|영웅 성장과 모집, 스킬 경험치 책, 영웅 경험치 및 UR/SSR/SR 영웅 조각.|英雄培养与招募、技能经验书、英雄经验及UR/SSR/SR英雄碎片。
stage_desc_5|Train T1–T10 troops; use training, building and research speedups; gain construction and research power.|Entraîner des troupes T1–T10 ; utiliser des accélérations d'entraînement, de construction et de recherche ; gagner de la puissance de construction et de recherche.|Подготовка войск T1–T10; ускорения подготовки, строительства и исследований; рост силы строительства и исследований.|T1–T10 asker eğitimi; eğitim, inşaat ve araştırma hızlandırmaları; inşaat ve araştırma gücü kazanımı.|Szkolenie oddziałów T1–T10; przyspieszenia szkolenia, budowy i badań; wzrost mocy budowy i badań.|Entrenar tropas T1–T10; usar aceleraciones de entrenamiento, construcción e investigación; aumentar el poder de construcción e investigación.|Treinar tropas T1–T10; usar acelerações de treino, construção e investigação; ganhar poder de construção e investigação.|T1–T10-Truppen ausbilden; Ausbildungs-, Bau- und Forschungsbeschleunigungen nutzen; Bau- und Forschungsmacht steigern.|T1~T10 병사 훈련, 훈련·건설·연구 가속 사용 및 건설·연구 전투력 증가.|训练T1至T10部队，使用训练、建造与研究加速，提升建设与研究战力。
stage_desc_6|Cross-server raids, enemy eliminations and troop losses (T1–T10), healing speedups, UR missions and logistics.|Raids inter-serveurs, éliminations ennemies et pertes de troupes (T1–T10), accélérations de soins, missions UR et logistique.|Межсерверные рейды, уничтожение врагов и потери войск T1–T10, ускорения лечения, задания UR и логистика.|Sunucular arası baskınlar, düşman öldürme ve asker kayıpları (T1–T10), iyileştirme hızlandırmaları, UR görevleri ve lojistik.|Najazdy między serwerami, eliminacja wrogów i straty oddziałów (T1–T10), przyspieszenia leczenia, misje UR i logistyka.|Incursiones entre servidores, bajas enemigas y propias (T1–T10), aceleraciones de curación, misiones UR y logística.|Incursões entre servidores, eliminações inimigas e perdas de tropas (T1–T10), acelerações de cura, missões UR e logística.|Serverübergreifende Raids, besiegte Feinde und Truppenverluste (T1–T10), Heilungsbeschleunigungen, UR-Missionen und Logistik.|서버 간 습격, 적 처치와 병사 손실(T1~T10), 치료 가속, UR 임무 및 물류.|跨服突袭、击败敌兵与士兵损失（T1至T10）、治疗加速、UR任务及物流。
alliance|Alliance|Alliance|Альянс|İttifak|Sojusz|Alianza|Aliança|Allianz|연맹|联盟
score_label|Match score|Score du duel|Счёт матча|Maç skoru|Wynik meczu|Marcador del duelo|Resultado do duelo|Spielstand|대결 점수|对决比分
consistency_hint|Coefficient of variation; lower is steadier.|Coefficient de variation ; plus il est bas, plus le joueur est régulier.|Коэффициент вариации: чем ниже, тем стабильнее.|Değişim katsayısı; düşük değer daha istikrarlıdır.|Współczynnik zmienności; niższy oznacza większą regularność.|Coeficiente de variación; cuanto menor, más regular.|Coeficiente de variação; quanto menor, mais regular.|Variationskoeffizient; niedriger bedeutet beständiger.|변동계수입니다. 낮을수록 더 꾸준합니다.|变异系数；越低越稳定。
checksum_hint|Weekly points compared with the sum of daily points.|Points hebdomadaires comparés à la somme des points quotidiens.|Очки за неделю в сравнении с суммой очков по дням.|Haftalık puanların günlük puan toplamıyla karşılaştırması.|Punkty tygodniowe porównane z sumą punktów dziennych.|Puntos semanales comparados con la suma de puntos diarios.|Pontos semanais comparados com a soma dos pontos diários.|Wochenpunkte im Vergleich zur Summe der Tagespunkte.|주간 포인트와 일별 포인트 합계를 비교합니다.|周积分与每日积分合计的比较。
missing_points|Missing points|Points manquants|Отсутствующие очки|Eksik puanlar|Brakujące punkty|Puntos ausentes|Pontos em falta|Fehlende Punkte|누락된 포인트|缺失积分
missing_names|Missing names|Noms manquants|Отсутствующие имена|Eksik adlar|Brakujące nazwy|Nombres ausentes|Nomes em falta|Fehlende Namen|누락된 이름|缺失名称
profile_absent|Not on the roster in the selected week; showing {date}.|Absent de l'effectif de la semaine sélectionnée ; affichage du {date}.|Нет в составе выбранной недели; показаны данные за {date}.|Seçilen haftanın kadrosunda yok; {date} gösteriliyor.|Nieobecny w składzie wybranego tygodnia; pokazano {date}.|No está en la plantilla de la semana seleccionada; se muestra {date}.|Ausente do plantel da semana selecionada; a mostrar {date}.|Nicht im Kader der gewählten Woche; angezeigt wird {date}.|선택한 주의 명단에 없습니다. {date} 기록을 표시합니다.|未在所选周的名单中；显示 {date} 的记录。
days_total|Daily total|Total des jours|Сумма по дням|Günlük toplam|Suma dni|Total diario|Total diário|Tagessumme|일별 합계|每日合计
depth_note|Players are ranked within each alliance; difference is home minus opponent.|Les joueurs sont classés au sein de chaque alliance ; l'écart est notre alliance moins l'adversaire.|Игроки ранжируются внутри каждого альянса; разница — наш альянс минус противник.|Oyuncular kendi ittifaklarında sıralanır; fark kendi ittifakımız eksi rakiptir.|Gracze są klasyfikowani w obrębie każdego sojuszu; różnica to nasz sojusz minus przeciwnik.|Los jugadores se clasifican dentro de cada alianza; la diferencia es nuestra alianza menos el rival.|Os jogadores são classificados dentro de cada aliança; a diferença é a nossa aliança menos o adversário.|Spieler werden innerhalb jeder Allianz gereiht; Differenz ist unsere Allianz minus Gegner.|각 연맹 내 순위로 비교합니다. 차이는 우리 연맹에서 상대를 뺀 값입니다.|玩家按各自联盟内排名比较；差值为我方减去对手。
live_history_note|Live weekly totals are provisional.|Les totaux hebdomadaires en cours sont provisoires.|Текущие недельные итоги предварительные.|Canlı haftalık toplamlar geçicidir.|Tygodniowe sumy na żywo są tymczasowe.|Los totales semanales en curso son provisionales.|Os totais semanais em curso são provisórios.|Laufende Wochensummen sind vorläufig.|진행 중인 주간 합계는 잠정적입니다.|实时周合计尚未确定。
snapshot|Snapshot|Instantané|Снимок|Kayıt|Migawka|Captura|Captura|Momentaufnahme|스냅샷|快照
snapshots|Snapshots|Instantanés|Снимки|Kayıtlar|Migawki|Capturas|Capturas|Momentaufnahmen|스냅샷|快照
source|Source|Source|Источник|Kaynak|Źródło|Fuente|Fonte|Quelle|출처|来源
approximate|approximate|approximatif|приблизительно|yaklaşık|przybliżony|aproximado|aproximado|ungefähr|대략|近似
local_time|Local time|Heure locale|Местное время|Yerel saat|Czas lokalny|Hora local|Hora local|Ortszeit|현지 시간|本地时间
server_time_short|server time|heure serveur|время сервера|sunucu saati|czas serwera|hora del servidor|hora do servidor|Serverzeit|서버 시간|服务器时间
snapshot_at|snapshot {time}|instantané {time}|снимок {time}|kayıt {time}|migawka {time}|captura {time}|captura {time}|Momentaufnahme {time}|스냅샷 {time}|快照 {time}
snapshot_server_time|Snapshot {time} server time|Instantané {time} heure serveur|Снимок {time} время сервера|Kayıt {time} sunucu saati|Migawka {time} czas serwera|Captura {time} hora del servidor|Captura {time} hora do servidor|Momentaufnahme {time} Serverzeit|스냅샷 {time} 서버 시간|快照 {time} 服务器时间
snapshot_window|Snapshot: {first} – {last} · server time (UTC−2)|Instantané : {first} – {last} · heure serveur (UTC−2)|Снимок: {first} – {last} · время сервера (UTC−2)|Kayıt: {first} – {last} · sunucu saati (UTC−2)|Migawka: {first} – {last} · czas serwera (UTC−2)|Captura: {first} – {last} · hora del servidor (UTC−2)|Captura: {first} – {last} · hora do servidor (UTC−2)|Momentaufnahme: {first} – {last} · Serverzeit (UTC−2)|스냅샷: {first} – {last} · 서버 시간 (UTC−2)|快照：{first} – {last} · 服务器时间（UTC−2）
source_screenshots|Screenshots|Captures d'écran|Снимки экрана|Ekran görüntüleri|Zrzuty ekranu|Capturas de pantalla|Capturas de ecrã|Bildschirmaufnahmen|캡처 화면|截图
source_capture_log|Capture log|Journal de capture|Журнал захвата|Kayıt günlüğü|Dziennik zapisu|Registro de captura|Registo de captura|Erfassungsprotokoll|캡처 로그|采集日志
source_legacy_file_times|Legacy file times|Dates des anciens fichiers|Время старых файлов|Eski dosya zamanları|Daty starych plików|Fechas de archivos antiguos|Datas dos ficheiros legados|Zeitstempel alter Dateien|기존 파일 타임스탬프|历史文件时间
"""


def translations():
    result = {lang: dict(values) for lang, values in T.items()}
    for line in TRANSLATIONS.strip().splitlines():
        key, *values = line.split('|')
        if len(values) != len(LOCALES):
            raise ValueError(f'{key}: expected {len(LOCALES)} translations, got {len(values)}')
        for lang, value in zip(LOCALES, values):
            if key in result[lang]:
                raise ValueError(f'Duplicate key: {lang}.{key}')
            result[lang][key] = value
    keys = set(result['en'])
    for lang, values in result.items():
        if set(values) != keys:
            raise ValueError(f'{lang}: translation keys differ')
        for key, value in values.items():
            if not value.strip():
                raise ValueError(f'{lang}.{key}: empty translation')
            if sorted(re.findall(r'\{(\w+)\}', value)) != sorted(re.findall(r'\{(\w+)\}', result['en'][key])):
                raise ValueError(f'{lang}.{key}: placeholders differ')
    return result


def build():
    result = translations()
    i18n_path = ROOT / 'data' / 'i18n.js'
    i18n_path.write_text(
        '// Generated by pipeline/build_i18n.py; edit the generator.\n'
        + 'window.I18N = ' + json.dumps(result, ensure_ascii=False, indent=2) + ';\n'
        + 'window.LANG_LOCALES = ' + json.dumps(LOCALES, ensure_ascii=False) + ';\n'
        + 'window.LANG_NAMES = ' + json.dumps(NAMES, ensure_ascii=False) + ';\n',
        encoding='utf-8',
    )
    stages = json.loads((ROOT / 'data' / 'competition_stages.json').read_text(encoding='utf-8'))
    stages_path = ROOT / 'data' / 'stages.js'
    stages_content = (
        '// Generated by pipeline/build_i18n.py from competition_stages.json.\n'
        + 'window.VS_STAGES = ' + json.dumps(stages, ensure_ascii=False, indent=2) + ';\n'
    )
    if not stages_path.exists() or stages_path.read_text(encoding='utf-8') != stages_content:
        stages_path.write_text(stages_content, encoding='utf-8')
    print(f'Generated {len(result)} languages × {len(result["en"])} keys and {len(stages["stages"])} stages')
    # Match the sister site: refresh asset hashes whenever translations are rebuilt.
    # build_week.py also invokes this stamper after rebuilding manifest data.
    stamper = ROOT / 'pipeline' / 'stamp_assets.py'
    if stamper.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location('vs_stamp_assets', stamper)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.stamp()


if __name__ == '__main__':
    build()
