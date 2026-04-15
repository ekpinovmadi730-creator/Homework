#   ОЙЫН СТАТИСТИКАСЫ — Game Statistics Analysis
#   Кітапханалар: NumPy + Pandas + Matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 1. NumPy арқылы деректерді ГЕНЕРАЦИЯЛАУ

np.random.seed(42)

oyynshylar = [
    "Aibek", "Saltanat", "Dauren", "Meruert", "Nurlan",
    "Ainur", "Bekzat", "Zarina", "Temirlan", "Aliya"
]

n = len(oyynshylar)

upay    = np.random.randint(3000, 10000, size=n)
uaqyt   = np.random.randint(20,   90,    size=n)
denghey = np.random.randint(1,    20,    size=n)

print("=" * 55)
print("1. NumPy генерацияланған деректер (raw arrays)")
print("=" * 55)
print(f"  Ұпай    : {upay}")
print(f"  Уақыт   : {uaqyt}")
print(f"  Деңгей  : {denghey}")
# 2. Pandas DataFrame ҚҰРУ
df = pd.DataFrame({
    "Ойыншы":  oyynshylar,
    "Ұпай":    upay,
    "Уақыт":   uaqyt,
    "Деңгей":  denghey
})

print("\n" + "=" * 55)
print("2. Pandas DataFrame")
print("=" * 55)
print(df.to_string(index=False))
# 3. ЖАҢА БАҒАН ҚОСУ — GPA
df["Ұпай_%"]   = (df["Ұпай"]  / df["Ұпай"].max()  * 100).round(2)
df["Уақыт_%"]  = ((1 - df["Уақыт"] / df["Уақыт"].max()) * 100).round(2)
df["Деңгей_%"] = (df["Деңгей"] / df["Деңгей"].max() * 100).round(2)

df["GPA"] = df[["Ұпай_%", "Уақыт_%", "Деңгей_%"]].mean(axis=1).round(2)

print("\n" + "=" * 55)
print("3. Жаңа баған: GPA (0–100 шкала)")
print("=" * 55)
print(df[["Ойыншы", "Ұпай", "Уақыт", "Деңгей", "GPA"]].to_string(index=False))
# 4. ФИЛЬТРАЦИЯ
uzdik  = df[df["GPA"] >= 70]
nashar = df[df["GPA"] <  50]

print("\n" + "=" * 55)
print("4a. Фильтр: Үздік ойыншылар (GPA >= 70)")
print("=" * 55)
print(uzdik[["Ойыншы", "Ұпай", "Деңгей", "GPA"]].to_string(index=False))

print("\n4b. Фильтр: Нашар ойыншылар (GPA < 50)")
print("-" * 55)
if nashar.empty:
    print("  Мұндай ойыншылар жоқ.")
else:
    print(nashar[["Ойыншы", "Ұпай", "Деңгей", "GPA"]].to_string(index=False))
# 5. СҰРЫПТАУ
df_sorted = df.sort_values(by="GPA", ascending=False).reset_index(drop=True)
df_sorted.index += 1
print("\n" + "=" * 55)
print("5. Сұрыптау: GPA бойынша рейтинг")
print("=" * 55)
print(df_sorted[["Ойыншы", "Ұпай", "Уақыт", "Деңгей", "GPA"]].to_string())
# 6. GROUPBY
def kategoriya(gpa):
    if   gpa >= 80: return "A — Үздік"
    elif gpa >= 65: return "B — Жақсы"
    elif gpa >= 50: return "C — Қанағат"
    else:           return "D — Нашар"

df["Категория"] = df["GPA"].apply(kategoriya)

groupby_df = (
    df.groupby("Категория")[["Ұпай", "Уақыт", "Деңгей", "GPA"]]
    .agg(["mean", "count"])
    .round(2)
)
print("\n" + "=" * 55)
print("6. GroupBy: Категория бойынша статистика")
print("=" * 55)
print(groupby_df)
# 7. NumPy ҚОСЫМША ТАЛДАУ
upay_arr = df["Ұпай"].to_numpy()
gpa_arr  = df["GPA"].to_numpy()
print("\n" + "=" * 55)
print("7. NumPy қосымша талдауы")
print("=" * 55)
print(f"  Ұпай — орташа     : {np.mean(upay_arr):.1f}")
print(f"  Ұпай — медиана    : {np.median(upay_arr):.1f}")
print(f"  Ұпай — std        : {np.std(upay_arr):.1f}")
print(f"  Ұпай — min / max  : {np.min(upay_arr)} / {np.max(upay_arr)}")
print(f"  GPA  — орташа     : {np.mean(gpa_arr):.2f}")
print(f"  GPA  — 25th перц  : {np.percentile(gpa_arr, 25):.2f}")
print(f"  GPA  — 75th перц  : {np.percentile(gpa_arr, 75):.2f}")
korr = np.corrcoef(upay_arr, gpa_arr)[0, 1]
print(f"  Ұпай–GPA корреляция: {korr:.4f}")
best_idx  = np.argmax(gpa_arr)
best_name = df.loc[best_idx, "Ойыншы"]
best_gpa  = df.loc[best_idx, "GPA"]
print(f"\n  🏆 ЕҢ ҮЗДІК ОЙЫНШЫ: {best_name}  (GPA = {best_gpa})")
# 8. ВИЗУАЛИЗАЦИЯ
fig, axes = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle("Ойын Статистикасы / Game Statistics",
             fontsize=15, fontweight="bold")

bar_colors = ["#4CAF50" if g >= 70 else "#FF9800" if g >= 50 else "#F44336"
              for g in df_sorted["GPA"]]
# График 1 — GPA рейтингі
ax1 = axes[0, 0]
bars = ax1.barh(df_sorted["Ойыншы"], df_sorted["GPA"],
                color=bar_colors, edgecolor="white", height=0.6)
ax1.axvline(np.mean(gpa_arr), color="navy", linestyle="--",
            linewidth=1.5, label=f"Орташа: {np.mean(gpa_arr):.1f}")
ax1.set_title("GPA Рейтингі")
ax1.set_xlabel("GPA")
ax1.legend(fontsize=8)
ax1.invert_yaxis()
for b, v in zip(bars, df_sorted["GPA"]):
    ax1.text(b.get_width() + 0.5, b.get_y() + b.get_height()/2,
             f"{v:.1f}", va="center", fontsize=8)
# График 2 — Ұпай vs Деңгей
ax2 = axes[0, 1]
sc = ax2.scatter(df["Деңгей"], df["Ұпай"], c=df["GPA"],
                 cmap="RdYlGn", s=130, edgecolors="gray",
                 linewidths=0.5, vmin=0, vmax=100)
for _, row in df.iterrows():
    ax2.annotate(row["Ойыншы"], (row["Деңгей"], row["Ұпай"]),
                 fontsize=7, xytext=(4, 4), textcoords="offset points")
ax2.set_xlabel("Деңгей / Level")
ax2.set_ylabel("Ұпай / Score")
ax2.set_title("Деңгей vs Ұпай")
plt.colorbar(sc, ax=ax2, label="GPA")
# График 3 — Категория (дөңгелек)
ax3 = axes[1, 0]
cat_cnt = df["Категория"].value_counts()
ax3.pie(cat_cnt, labels=cat_cnt.index, autopct="%1.0f%%",
        colors=["#4CAF50", "#2196F3", "#FF9800", "#F44336"][:len(cat_cnt)],
        startangle=90, wedgeprops=dict(edgecolor="white", linewidth=1.5))
ax3.set_title("Категориялар")
# График 4 — Уақыт vs GPA
ax4 = axes[1, 1]
df_t = df.sort_values("Уақыт")
ax4.plot(df_t["Уақыт"], df_t["GPA"], "o-", color="#9C27B0",
         linewidth=2, markersize=7,
         markerfacecolor="white", markeredgewidth=2)
ax4.set_xlabel("Уақыт (мин)")
ax4.set_ylabel("GPA")
ax4.set_title("Уақыт vs GPA")
ax4.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("game_stats_chart.png", dpi=150, bbox_inches="tight")
print("\n  Графиктер сақталды: game_stats_chart.png")
plt.show()
# 9. CSV ФАЙЛҒА САҚТАУ
final_df = df[["Ойыншы", "Ұпай", "Уақыт", "Деңгей", "GPA", "Категория"]] \
             .sort_values("GPA", ascending=False) \
             .reset_index(drop=True)
final_df.to_csv("game_stats_result.csv", index=False, encoding="utf-8-sig")
print("  CSV сақталды: game_stats_result.csv")
print("\n Барлық тапсырмалар орындалды!")