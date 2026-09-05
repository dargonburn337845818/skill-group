using System;
using System.Drawing;
using System.IO;
using System.Diagnostics;
using System.Text.RegularExpressions;
using Microsoft.Win32;
using System.Windows.Forms;

namespace NvidiaTuningPanel
{
    public class PillBar : Control
    {
        private int _value;
        public int Value { get { return _value; } set { _value = value; Invalidate(); } }
        public int Max { get; set; }
        public Color FillColor { get; set; }
        public Color TrackColor { get; set; }

        public PillBar()
        {
            DoubleBuffered = true;
            Height = 8;
            Max = 100;
            FillColor = SystemColors.Highlight;
            TrackColor = SystemColors.ControlDark;
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            e.Graphics.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
            var r = ClientRectangle;
            if (r.Height <= 0) return;
            int radius = r.Height / 2;
            using (var path = RoundRect(r, radius))
            using (var brush = new SolidBrush(TrackColor))
            {
                e.Graphics.FillPath(brush, path);
            }
            if (Value > 0 && Max > 0)
            {
                int w = (int)(r.Width * (double)Value / Max);
                if (w > 0)
                {
                    var fillRect = new Rectangle(r.X, r.Y, w, r.Height);
                    using (var path = RoundRect(fillRect, radius))
                    using (var brush = new SolidBrush(FillColor))
                    {
                        e.Graphics.FillPath(brush, path);
                    }
                }
            }
        }

        private System.Drawing.Drawing2D.GraphicsPath RoundRect(Rectangle r, int radius)
        {
            var path = new System.Drawing.Drawing2D.GraphicsPath();
            int d = radius * 2;
            path.AddArc(r.X, r.Y, d, d, 180, 90);
            path.AddArc(r.Right - d, r.Y, d, d, 270, 90);
            path.AddArc(r.Right - d, r.Bottom - d, d, d, 0, 90);
            path.AddArc(r.X, r.Bottom - d, d, d, 90, 90);
            path.CloseFigure();
            return path;
        }
    }

    public enum MetricKind
    {
        Gpu,
        Temp,
        Power,
        Vram,
        Mem,
        Cpu
    }

    public class MetricIcon : Control
    {
        public MetricKind Kind { get; set; }
        public Color IconColor { get; set; }

        public MetricIcon()
        {
            DoubleBuffered = true;
            Width = 20;
            Height = 20;
            SetStyle(ControlStyles.SupportsTransparentBackColor, true);
            BackColor = Color.Transparent;
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            if (IconColor == Color.Empty) return;
            e.Graphics.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
            var g = e.Graphics;
            using (var pen = new Pen(IconColor, 1.4F))
            using (var brush = new SolidBrush(IconColor))
            {
                switch (Kind)
                {
                    case MetricKind.Gpu:
                        g.DrawArc(pen, 1, 4, 18, 18, 200, 140);
                        g.DrawLine(pen, 10, 12, 15, 6);
                        g.FillEllipse(brush, 8, 10, 4, 4);
                        break;
                    case MetricKind.Temp:
                        g.DrawRectangle(pen, 8, 2, 4, 10);
                        g.FillEllipse(brush, 6, 12, 8, 8);
                        break;
                    case MetricKind.Power:
                        g.DrawEllipse(pen, 3, 6, 14, 14);
                        g.DrawLine(pen, 10, 3, 10, 12);
                        break;
                    case MetricKind.Vram:
                    case MetricKind.Mem:
                        g.DrawRectangle(pen, 3, 5, 14, 8);
                        for (int i = 0; i < 4; i++)
                        {
                            int x = 5 + i * 3;
                            g.DrawLine(pen, x, 13, x, 17);
                        }
                        g.FillRectangle(brush, 5, 7, 3, 3);
                        g.FillRectangle(brush, 10, 7, 3, 3);
                        break;
                    case MetricKind.Cpu:
                        g.DrawRectangle(pen, 4, 4, 12, 12);
                        g.DrawRectangle(pen, 7, 7, 6, 6);
                        for (int i = 0; i < 3; i++)
                        {
                            int y = 6 + i * 4;
                            g.DrawLine(pen, 2, y, 4, y);
                            g.DrawLine(pen, 16, y, 18, y);
                            g.DrawLine(pen, y, 2, y, 4);
                            g.DrawLine(pen, y, 16, y, 18);
                        }
                        break;
                }
            }
        }
    }

    public class CardPanel : Panel
    {
        public Color BorderColor { get; set; }

        public CardPanel()
        {
            DoubleBuffered = true;
            BorderColor = Color.FromArgb(44, 44, 44);
            SetStyle(ControlStyles.UserPaint | ControlStyles.AllPaintingInWmPaint | ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw, true);
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);
            if (Width <= 4 || Height <= 4) return;
            e.Graphics.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
            var rect = new Rectangle(2, 2, Width - 5, Height - 5);
            using (var pen = new Pen(BorderColor, 2F) { DashStyle = System.Drawing.Drawing2D.DashStyle.Dash })
            {
                e.Graphics.DrawRectangle(pen, rect);
            }
            // cross-hatch sketch shadow (bottom-right)
            using (var shadow = new Pen(Color.FromArgb(70, BorderColor), 1F))
            {
                int x0 = rect.Right - 2;
                for (int i = 0; i < 5; i++)
                {
                    e.Graphics.DrawLine(shadow, x0 - i * 3, rect.Bottom - i * 2, x0 - i * 3 - 6, rect.Bottom - i * 2 + 6);
                }
            }
        }
    }

    public class SketchChart : Control
    {
        private System.Collections.Generic.List<double> gpuSeries;
        private System.Collections.Generic.List<double> tempSeries;
        private System.Collections.Generic.List<double> powerSeries;
        private System.Collections.Generic.List<double> memSeries;
        private System.Collections.Generic.List<double> cpuSeries;
        private static readonly Color SeriesRed = Color.FromArgb(231, 76, 60);
        private static readonly Color SeriesBlue = Color.FromArgb(52, 152, 219);
        private static readonly Color SeriesGreen = Color.FromArgb(39, 174, 96);
        private static readonly Color SeriesYellow = Color.FromArgb(243, 156, 18);
        private static readonly Color SeriesGray = Color.FromArgb(140, 140, 140);
        private int maxPoints;

        public SketchChart()
        {
            DoubleBuffered = true;
            maxPoints = 120;
            gpuSeries = new System.Collections.Generic.List<double>();
            tempSeries = new System.Collections.Generic.List<double>();
            powerSeries = new System.Collections.Generic.List<double>();
            memSeries = new System.Collections.Generic.List<double>();
            cpuSeries = new System.Collections.Generic.List<double>();
            SetStyle(ControlStyles.UserPaint | ControlStyles.AllPaintingInWmPaint | ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw, true);
        }

        public void AddSample(double gpu, double temp, double power, double mem, double cpu)
        {
            gpuSeries.Add(gpu); tempSeries.Add(temp); powerSeries.Add(power); memSeries.Add(mem); cpuSeries.Add(cpu);
            if (gpuSeries.Count > maxPoints) gpuSeries.RemoveAt(0);
            if (tempSeries.Count > maxPoints) tempSeries.RemoveAt(0);
            if (powerSeries.Count > maxPoints) powerSeries.RemoveAt(0);
            if (memSeries.Count > maxPoints) memSeries.RemoveAt(0);
            if (cpuSeries.Count > maxPoints) cpuSeries.RemoveAt(0);
            Invalidate();
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);
            var g = e.Graphics;
            g.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
            if (Width < 40 || Height < 40) return;
            var r = ClientRectangle;
            // paper background
            using (var bg = new SolidBrush(Color.FromArgb(253, 249, 241)))
                g.FillRectangle(bg, r);
            // dashed border
            using (var pen = new Pen(Color.FromArgb(44, 44, 44), 2F) { DashStyle = System.Drawing.Drawing2D.DashStyle.Dash })
                g.DrawRectangle(pen, 1, 1, Width - 3, Height - 3);
            // grid
            using (var gridPen = new Pen(Color.FromArgb(50, 138, 133, 128), 1F))
            {
                for (int i = 1; i < 4; i++)
                {
                    int y = r.Top + (r.Height - 26) * i / 4 + 16;
                    g.DrawLine(gridPen, r.Left + 34, y, r.Right - 8, y);
                }
            }
            // legend
            using (var f = new Font("KaiTi", 8.5F))
            using (var textBrush = new SolidBrush(Color.FromArgb(44, 44, 44)))
            {
                g.DrawString("GPU", f, new SolidBrush(SeriesRed), 36, 4);
                g.DrawString("CPU", f, new SolidBrush(SeriesBlue), 80, 4);
                g.DrawString("MEM", f, new SolidBrush(SeriesGreen), 124, 4);
                g.DrawString("TEMP", f, new SolidBrush(SeriesYellow), 168, 4);
                g.DrawString("PWR", f, new SolidBrush(Color.FromArgb(120, 120, 120)), 224, 4);
            }
            int n = gpuSeries.Count;
            if (n < 2) return;
            int left = 34, right = r.Right - 8, top = 18, bottom = r.Bottom - 10;
            if (right - left < 10 || bottom - top < 10) return;
            DrawSeries(g, left, top, right, bottom, gpuSeries, 0, 100, SeriesRed, 2F);
            DrawSeries(g, left, top, right, bottom, cpuSeries, 0, 100, SeriesBlue, 2F);
            DrawSeries(g, left, top, right, bottom, memSeries, 0, 100, SeriesGreen, 2F);
            DrawSeries(g, left, top, right, bottom, tempSeries, 0, 100, SeriesYellow, 2F);
            DrawSeries(g, left, top, right, bottom, powerSeries, 0, 150, Color.FromArgb(140, 140, 140), 1.5F);
        }

        private void DrawSeries(Graphics g, int left, int top, int right, int bottom, System.Collections.Generic.List<double> data, double minV, double maxV, Color color, float width)
        {
            if (data.Count < 2) return;
            float xStep = (float)(right - left) / (data.Count - 1);
            using (var pen = new Pen(color, width) { DashStyle = System.Drawing.Drawing2D.DashStyle.Solid })
            {
                for (int i = 1; i < data.Count; i++)
                {
                    float x1 = left + (i - 1) * xStep;
                    float x2 = left + i * xStep;
                    float y1 = Scale(data[i - 1], minV, maxV, top, bottom);
                    float y2 = Scale(data[i], minV, maxV, top, bottom);
                    g.DrawLine(pen, x1, y1, x2, y2);
                }
            }
        }

        private float Scale(double v, double minV, double maxV, int top, int bottom)
        {
            if (maxV <= minV) return top;
            double t = (v - minV) / (maxV - minV);
            if (t < 0) t = 0; if (t > 1) t = 1;
            return bottom - (float)(t * (bottom - top));
        }
    }

   public class MainForm : Form
    {
        private Label lblMode;
        private Label lblScheduler;
        private Label lblStatusLine;
        private TextBox txtLog;
        private PillBar barGpu, barTemp, barPower, barVram, barMem, barCpu;
        private Label valGpu, valTemp, valPower, valVram, valMem, valCpu;
        private Button btnStart, btnStop, btnRefresh, btnApply, btnRestore, btnMemClean, btnHelp, btnExit;
        private Button btnTheme;
        private SketchChart historyChart;
        private double curGpu, curTemp, curPower, curMem, curCpu;
        private Timer autoTimer;
        private NotifyIcon notifyIcon;
        private bool exitRequested = false;
        private bool darkTheme = false;
        private volatile bool refreshingAsync = false;
        private static string ThemeRegPath = @"Software\NvidiaTuningPanel";
        private static string ThemeValueName = "DarkTheme";

        private string schedulerPs = @"D:\<工具目录>\optimizer\GHelperSmartScheduler.ps1";
        private string statusPs = @"D:\<工具目录>\optimizer\status-report.ps1";
        private string localOptPs = @"D:\<工具目录>\local-optimizer\LocalOptimizer.ps1";
        private string restorePs = @"D:\<工具目录>\local-optimizer\LocalOptimizer.restore.ps1";
        private string memReductExe = @"D:\<内存工具目录>\Mem Reduct\memreduct.exe";

        private static Color Bg = Color.FromArgb(245, 240, 232);
        private static Color Card = Color.FromArgb(253, 249, 241);
        private static Color SurfaceAlt = Color.FromArgb(245, 240, 232);
        private static Color Line = Color.FromArgb(44, 44, 44);
        private static Color BorderSoft = Color.FromArgb(138, 133, 128);
        private static Color Ink = Color.FromArgb(44, 44, 44);
        private static Color Muted = Color.FromArgb(107, 107, 107);
        private static Color Accent = Color.FromArgb(44, 44, 44);
        private static Color AccentHover = Color.FromArgb(26, 26, 26);
        private static Color OnAccent = Color.FromArgb(245, 240, 232);
        private static Color Success = Color.FromArgb(39, 174, 96);
        private static Color Warning = Color.FromArgb(243, 156, 18);
        private static Color Danger = Color.FromArgb(231, 76, 60);
        private static Color Info = Color.FromArgb(52, 152, 219);
        private static Color SketchRed = Color.FromArgb(231, 76, 60);
        private static Color SketchBlue = Color.FromArgb(52, 152, 219);
        private static Color SketchGreen = Color.FromArgb(39, 174, 96);
        private static Color SketchYellow = Color.FromArgb(243, 156, 18);

        public MainForm()
        {
            Text = "NVIDIA 调优";
            ClientSize = new Size(960, 760);
            MinimumSize = new Size(960, 760);
            StartPosition = FormStartPosition.CenterScreen;
            BackColor = Bg;
            Font = new Font("KaiTi", 10.5F);
            AutoScaleMode = AutoScaleMode.Dpi;
            AutoScaleDimensions = new SizeF(96F, 96F);

            LoadTheme();
            SetThemeColors(darkTheme);
            BuildUi();
            Load += (s, e) => FitToScreen();
            RefreshData();

            autoTimer = new Timer();
            autoTimer.Interval = 5000;
            autoTimer.Tick += (s, e) => RefreshDataAsync();
            autoTimer.Start();

            SetupTray();
            Icon = CreateAppIcon();
            // 启动默认显示主窗口；关闭时仍最小化到托盘。
            ShowInTaskbar = true;
        }

        private static Bitmap CreateGlyphImage(string glyph, int size, Color color)
        {
            var bmp = new Bitmap(size, size);
            using (var g = Graphics.FromImage(bmp))
            {
                g.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
                g.Clear(Color.Transparent);
                using (var font = new Font("Segoe MDL2 Assets", size - 4, FontStyle.Regular, GraphicsUnit.Pixel))
                using (var brush = new SolidBrush(color))
                {
                    var sf = new StringFormat();
                    sf.Alignment = StringAlignment.Center;
                    sf.LineAlignment = StringAlignment.Center;
                    var rect = new RectangleF(0, 0, size, size);
                    g.DrawString(glyph, font, brush, rect, sf);
                }
            }
            return bmp;
        }

        private void LoadTheme()
        {
            try
            {
                using (var key = Registry.CurrentUser.OpenSubKey(ThemeRegPath))
                {
                    if (key != null)
                    {
                        object v = key.GetValue(ThemeValueName);
                        if (v != null)
                        {
                            darkTheme = Convert.ToInt32(v) == 1;
                            return;
                        }
                    }
                }
                using (var key = Registry.CurrentUser.OpenSubKey(@"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"))
                {
                    if (key != null)
                    {
                        object v = key.GetValue("AppsUseLightTheme");
                        if (v != null)
                        {
                            darkTheme = Convert.ToInt32(v) == 0;
                            return;
                        }
                    }
                }
            }
            catch { }
            darkTheme = false;
        }

        private void SaveTheme()
        {
            try
            {
                using (var key = Registry.CurrentUser.CreateSubKey(ThemeRegPath))
                {
                    if (key != null) key.SetValue(ThemeValueName, darkTheme ? 1 : 0, RegistryValueKind.DWord);
                }
            }
            catch { }
        }

        private static void SetThemeColors(bool dark)
        {
            if (dark)
            {
                Bg = Color.FromArgb(43, 39, 33);
                Card = Color.FromArgb(53, 48, 42);
                SurfaceAlt = Color.FromArgb(43, 39, 33);
                Line = Color.FromArgb(216, 207, 192);
                BorderSoft = Color.FromArgb(167, 159, 147);
                Ink = Color.FromArgb(241, 234, 224);
                Muted = Color.FromArgb(189, 180, 166);
                Accent = Color.FromArgb(241, 234, 224);
                AccentHover = Color.FromArgb(255, 255, 255);
                OnAccent = Color.FromArgb(43, 39, 33);
                Success = Color.FromArgb(108, 203, 95);
                Warning = Color.FromArgb(255, 212, 0);
                Danger = Color.FromArgb(255, 107, 107);
                Info = Color.FromArgb(86, 182, 239);
            }
            else
            {
                Bg = Color.FromArgb(245, 240, 232);
                Card = Color.FromArgb(253, 249, 241);
                SurfaceAlt = Color.FromArgb(245, 240, 232);
                Line = Color.FromArgb(44, 44, 44);
                BorderSoft = Color.FromArgb(138, 133, 128);
                Ink = Color.FromArgb(44, 44, 44);
                Muted = Color.FromArgb(107, 107, 107);
                Accent = Color.FromArgb(44, 44, 44);
                AccentHover = Color.FromArgb(26, 26, 26);
                OnAccent = Color.FromArgb(245, 240, 232);
                Success = Color.FromArgb(39, 174, 96);
                Warning = Color.FromArgb(243, 156, 18);
                Danger = Color.FromArgb(231, 76, 60);
                Info = Color.FromArgb(52, 152, 219);
            }
        }

        private void ApplyTheme(bool dark)
        {
            if (darkTheme == dark) return;
            darkTheme = dark;
            SetThemeColors(dark);
            SaveTheme();
            string log = txtLog == null ? "" : txtLog.Text;
            Controls.Clear();
            BuildUi();
            if (txtLog != null && log.Length > 0) txtLog.Text = log;
            RefreshData();
            if (notifyIcon != null) notifyIcon.Icon = CreateAppIcon();
        }

        private void BuildUi()
        {
            SuspendLayout();

            var root = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, RowCount = 1, Margin = new Padding(0), Padding = new Padding(0) };
            root.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 200));
            root.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
            root.RowStyles.Add(new RowStyle(SizeType.Percent, 100));

            // 左侧
            var sidebar = new Panel { Dock = DockStyle.Fill, BackColor = SurfaceAlt, Padding = new Padding(20, 20, 16, 16) };
            BuildSidebar(sidebar);
            root.Controls.Add(sidebar, 0, 0);

            // 右侧
            var right = new Panel { Dock = DockStyle.Fill, Padding = new Padding(24, 20, 24, 20), BackColor = Bg };
            var layout = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 1, RowCount = 5, Margin = new Padding(0), Padding = new Padding(0) };
            layout.RowStyles.Add(new RowStyle(SizeType.Absolute, 64));
            layout.RowStyles.Add(new RowStyle(SizeType.Absolute, 300));
            layout.RowStyles.Add(new RowStyle(SizeType.Absolute, 100));
            layout.RowStyles.Add(new RowStyle(SizeType.Absolute, 200));
            layout.RowStyles.Add(new RowStyle(SizeType.Percent, 100));
            right.Controls.Add(layout);
            root.Controls.Add(right, 1, 0);
            Controls.Add(root);

            // 标题区
            var header = new Panel { Dock = DockStyle.Fill, BackColor = Color.Transparent };
            var headerLayout = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 1, RowCount = 2, Margin = new Padding(0), Padding = new Padding(0) };
            headerLayout.RowStyles.Add(new RowStyle(SizeType.Absolute, 38));
            headerLayout.RowStyles.Add(new RowStyle(SizeType.Absolute, 24));
            var title = new Label
            {
                Text = "实时数据",
                Font = new Font("KaiTi", 15F, FontStyle.Bold),
                ForeColor = Ink,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleLeft
            };
            lblStatusLine = new Label
            {
                Text = "自动刷新 5 秒 · 数据来自 nvidia-smi / WMI",
                Font = new Font("KaiTi", 9F),
                ForeColor = Muted,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleLeft
            };
            headerLayout.Controls.Add(title, 0, 0);
            headerLayout.Controls.Add(lblStatusLine, 0, 1);
            header.Controls.Add(headerLayout);
            layout.Controls.Add(header, 0, 0);

            // 指标卡片区
            var grid = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, RowCount = 3, Margin = new Padding(0), Padding = new Padding(0) };
            for (int i = 0; i < 2; i++) grid.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50));
            for (int i = 0; i < 3; i++) grid.RowStyles.Add(new RowStyle(SizeType.Percent, 33));
            layout.Controls.Add(grid, 0, 1);

            var cGpu = CreateMetric("GPU 利用率", MetricKind.Gpu, ref valGpu, ref barGpu, Accent);
            var cTemp = CreateMetric("GPU 温度", MetricKind.Temp, ref valTemp, ref barTemp, Accent);
            var cPower = CreateMetric("GPU 功耗", MetricKind.Power, ref valPower, ref barPower, Accent);
            var cVram = CreateMetric("显存占用", MetricKind.Vram, ref valVram, ref barVram, Accent);
            var cMem = CreateMetric("内存占用", MetricKind.Mem, ref valMem, ref barMem, Accent);
            var cCpu = CreateMetric("CPU 负载", MetricKind.Cpu, ref valCpu, ref barCpu, Accent);
            grid.Controls.Add(cGpu, 0, 0);
            grid.Controls.Add(cTemp, 1, 0);
            grid.Controls.Add(cPower, 0, 1);
            grid.Controls.Add(cVram, 1, 1);
            grid.Controls.Add(cMem, 0, 2);
            grid.Controls.Add(cCpu, 1, 2);

            // 操作区
            var actions = new FlowLayoutPanel { Dock = DockStyle.Fill, FlowDirection = FlowDirection.LeftToRight, WrapContents = true, Padding = new Padding(0, 8, 0, 8), Margin = new Padding(0) };
            actions.Controls.Add(MakeAction("启动", "\uE768", Accent, OnAccent, Color.Transparent, ref btnStart));
            actions.Controls.Add(MakeAction("停止", "\uE71A", Card, Danger, Danger, ref btnStop));
            actions.Controls.Add(MakeAction("优化", "\uE73E", Card, Accent, Accent, ref btnApply));
            actions.Controls.Add(MakeAction("回滚", "\uE7A7", Card, Warning, Warning, ref btnRestore));
            actions.Controls.Add(MakeAction("清内存", "\uE74D", Card, Info, Info, ref btnMemClean));
            actions.Controls.Add(MakeAction("刷新", "\uE72C", Card, Ink, BorderSoft, ref btnRefresh));
            actions.Controls.Add(MakeAction("说明", "\uE897", Card, Ink, BorderSoft, ref btnHelp));
            actions.Controls.Add(MakeAction("退出", "\uE8BB", Card, Ink, BorderSoft, ref btnExit));
            layout.Controls.Add(actions, 0, 2);

            // 趋势图区（图形化参数）
            historyChart = new SketchChart { Dock = DockStyle.Fill, Margin = new Padding(0, 8, 0, 4) };
            layout.Controls.Add(historyChart, 0, 3);

            // 日志区
            var logPanel = new CardPanel { Dock = DockStyle.Fill, BackColor = Card, BorderColor = Line, Padding = new Padding(14, 12, 14, 12) };
            var logTitle = new Label
            {
                Text = "最近日志",
                Font = new Font("KaiTi", 12F, FontStyle.Bold),
                ForeColor = Ink,
                Dock = DockStyle.Top,
                Height = 22,
                TextAlign = ContentAlignment.MiddleLeft
            };
            txtLog = new TextBox
            {
                Multiline = true,
                ReadOnly = true,
                ScrollBars = ScrollBars.Vertical,
                Font = new Font("KaiTi", 9F),
                Dock = DockStyle.Fill,
                BorderStyle = BorderStyle.None,
                BackColor = SurfaceAlt,
                ForeColor = Ink
            };
            logPanel.Controls.Add(txtLog);
            logPanel.Controls.Add(logTitle);
            layout.Controls.Add(logPanel, 0, 4);

            // 事件
            btnStart.Click += (s, e) => StartScheduler();
            btnStop.Click += (s, e) => StopScheduler();
            btnRefresh.Click += (s, e) => RefreshData(true);
            btnApply.Click += (s, e) => RunScript(localOptPs, "-Apply");
            btnRestore.Click += (s, e) => RunScript(restorePs, "");
            btnMemClean.Click += (s, e) => RunMemClean();
            btnHelp.Click += (s, e) => OpenDoc();
            btnExit.Click += (s, e) => Close();

            var tip = new ToolTip();
            tip.SetToolTip(btnStart, "后台启动 G-Helper 智能调度");
            tip.SetToolTip(btnStop, "停止调度并禁用开机自启");
            tip.SetToolTip(btnRefresh, "立即刷新数据");
            tip.SetToolTip(btnApply, "安全优化（自动备份）");
            tip.SetToolTip(btnRestore, "回滚最近一次优化");
            tip.SetToolTip(btnMemClean, "调用 Mem Reduct /clean:0x67");
            tip.SetToolTip(btnHelp, "打开优化说明");
            tip.SetToolTip(btnExit, "退出程序");

            ResumeLayout(true);
        }

        private void BuildSidebar(Panel sidebar)
        {
            var layout = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 1, RowCount = 5, Margin = new Padding(0), Padding = new Padding(0) };
            layout.RowStyles.Add(new RowStyle(SizeType.Absolute, 44));
            layout.RowStyles.Add(new RowStyle(SizeType.Absolute, 24));
            layout.RowStyles.Add(new RowStyle(SizeType.Absolute, 118));
            layout.RowStyles.Add(new RowStyle(SizeType.Absolute, 42));
            layout.RowStyles.Add(new RowStyle(SizeType.Percent, 100));

            var title = new Label
            {
                Text = "NVIDIA",
                Font = new Font("KaiTi", 15F, FontStyle.Bold),
                ForeColor = Ink,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleLeft
            };
            var sub = new Label
            {
                Text = "调优面板",
                Font = new Font("KaiTi", 9F),
                ForeColor = Muted,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleLeft
            };
            var statusCard = new CardPanel { Dock = DockStyle.Fill, BackColor = Card, BorderColor = Line, Padding = new Padding(14, 12, 14, 12), Margin = new Padding(0, 4, 0, 4) };
            var modeTitle = new Label
            {
                Text = "当前档位",
                Font = new Font("KaiTi", 9F),
                ForeColor = Muted,
                Dock = DockStyle.Top,
                Height = 20,
                TextAlign = ContentAlignment.MiddleLeft
            };
            lblMode = new Label
            {
                Text = "读取中",
                Font = new Font("KaiTi", 12F, FontStyle.Bold),
                ForeColor = Ink,
                Dock = DockStyle.Top,
                Height = 30,
                TextAlign = ContentAlignment.MiddleLeft
            };
            lblScheduler = new Label
            {
                Text = "调度器: ?",
                Font = new Font("KaiTi", 10.5F),
                ForeColor = Muted,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.TopLeft
            };
            statusCard.Controls.Add(lblScheduler);
            statusCard.Controls.Add(lblMode);
            statusCard.Controls.Add(modeTitle);

            btnTheme = MakeAction(darkTheme ? "浅色模式" : "暗色模式", "\uE706", Card, Ink, BorderSoft, ref btnTheme);
            btnTheme.Dock = DockStyle.Fill;
            btnTheme.Height = 34;
            btnTheme.Margin = new Padding(0, 4, 0, 4);
            btnTheme.Click += (s, e) => ApplyTheme(!darkTheme);

            var version = new Label
            {
                Text = "v0.4.0  面板 UI 重设计",
                Font = new Font("KaiTi", 9F),
                ForeColor = Muted,
                Dock = DockStyle.Bottom,
                Height = 24,
                TextAlign = ContentAlignment.MiddleLeft
            };
            layout.Controls.Add(title, 0, 0);
            layout.Controls.Add(sub, 0, 1);
            layout.Controls.Add(statusCard, 0, 2);
            layout.Controls.Add(btnTheme, 0, 3);
            layout.Controls.Add(version, 0, 4);
            sidebar.Controls.Add(layout);
        }

        private Panel CreateMetric(string name, MetricKind kind, ref Label valueLabel, ref PillBar bar, Color fill)
        {
            var card = new CardPanel { Dock = DockStyle.Fill, BackColor = Card, BorderColor = Line, Padding = new Padding(16, 12, 14, 14), Margin = new Padding(6) };
            var inner = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 1, RowCount = 3, Margin = new Padding(0), Padding = new Padding(0) };
            inner.RowStyles.Add(new RowStyle(SizeType.Absolute, 20));
            inner.RowStyles.Add(new RowStyle(SizeType.Absolute, 40));
            inner.RowStyles.Add(new RowStyle(SizeType.Percent, 100));

            var nameRow = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, RowCount = 1, Margin = new Padding(0), Padding = new Padding(0) };
            nameRow.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 24));
            nameRow.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
            var iconControl = new MetricIcon
            {
                Kind = kind,
                IconColor = Muted,
                Dock = DockStyle.Fill
            };
            var nameLabel = new Label
            {
                Text = name,
                Font = new Font("KaiTi", 9F),
                ForeColor = Muted,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleLeft
            };
            nameRow.Controls.Add(iconControl, 0, 0);
            nameRow.Controls.Add(nameLabel, 1, 0);

            valueLabel = new Label
            {
                Text = "--",
                Font = new Font("KaiTi", 16.5F, FontStyle.Bold),
                ForeColor = Ink,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleLeft
            };
            bar = new PillBar
            {
                Max = 100,
                Value = 0,
                Dock = DockStyle.Fill,
                Height = 8,
                Margin = new Padding(0, 8, 0, 0),
                FillColor = fill,
                TrackColor = Line
            };
            inner.Controls.Add(nameRow, 0, 0);
            inner.Controls.Add(valueLabel, 0, 1);
            inner.Controls.Add(bar, 0, 2);
            card.Controls.Add(inner);
            return card;
        }

        private Button MakeAction(string text, string glyph, Color back, Color fore, Color border, ref Button target)
        {
            bool hasBorder = border != Color.Transparent;
            Color normalBorderColor = hasBorder ? border : back;
            var b = new Button
            {
                Text = text,
                Image = CreateGlyphImage(glyph, 16, fore),
                TextImageRelation = TextImageRelation.ImageBeforeText,
                TextAlign = ContentAlignment.MiddleCenter,
                ImageAlign = ContentAlignment.MiddleLeft,
                Width = 100,
                Height = 34,
                Margin = new Padding(4),
                FlatStyle = FlatStyle.Flat,
                FlatAppearance = { BorderSize = hasBorder ? 1 : 0, BorderColor = normalBorderColor },
                BackColor = back,
                ForeColor = fore,
                Font = new Font("KaiTi", 10.5F, FontStyle.Bold),
                Cursor = Cursors.Hand
            };
            Color hoverBack = back;
            Color downBack = back;
            if (hasBorder)
            {
                hoverBack = darkTheme ? ControlPaint.Light(Card, 0.12F) : ControlPaint.Dark(Card, 0.08F);
                downBack = darkTheme ? ControlPaint.Dark(Card, 0.06F) : ControlPaint.Dark(Card, 0.14F);
            }
            else
            {
                hoverBack = darkTheme ? ControlPaint.Light(back, 0.12F) : ControlPaint.Dark(back, 0.08F);
                downBack = darkTheme ? ControlPaint.Dark(back, 0.08F) : ControlPaint.Dark(back, 0.16F);
            }
            b.FlatAppearance.MouseOverBackColor = hoverBack;
            b.FlatAppearance.MouseDownBackColor = downBack;

            Color normalBack = back;
            Color focusBack = hoverBack;
            Color focusBorder = hasBorder ? Accent : OnAccent;
            int normalBorderSize = hasBorder ? 1 : 0;
            b.GotFocus += (s, e) => { b.BackColor = focusBack; b.FlatAppearance.BorderColor = focusBorder; b.FlatAppearance.BorderSize = 2; };
            b.LostFocus += (s, e) => { b.BackColor = normalBack; b.FlatAppearance.BorderColor = normalBorderColor; b.FlatAppearance.BorderSize = normalBorderSize; };

            // 手绘虚线边框（覆盖在按钮上，保留 hover/pressed）
            b.Paint += (s2, e2) =>
            {
                var g = e2.Graphics;
                using (var pen = new Pen(normalBorderColor, 2F) { DashStyle = System.Drawing.Drawing2D.DashStyle.Dash })
                {
                    g.DrawRectangle(pen, 2, 2, b.Width - 5, b.Height - 5);
                }
            };

            target = b;
            return b;
        }

        private void RefreshDataAsync()
        {
            if (refreshingAsync) return;
            refreshingAsync = true;
            System.Threading.ThreadPool.QueueUserWorkItem(delegate
            {
                string raw = RunScriptRaw(statusPs, "");
                try
                {
                    if (IsHandleCreated)
                    {
                        BeginInvoke((Action)(delegate
                        {
                            ParseStatus(raw);
                            refreshingAsync = false;
                        }));
                    }
                    else
                    {
                        ParseStatus(raw);
                        refreshingAsync = false;
                    }
                }
                catch
                {
                    refreshingAsync = false;
                }
            });
        }

        private void RefreshData(bool verbose = false)
        {
            string raw = RunScriptRaw(statusPs, "");
            if (verbose) AppendLog(raw);
            ParseStatus(raw);
        }

        private void ParseStatus(string raw)
        {
            string[] lines = raw.Split(new[] { '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries);
            foreach (var line in lines)
            {
                string t = Regex.Replace(line.Trim(), @"\s+", " ");
                if (t.StartsWith("当前 G-Helper 档位"))
                {
                    lblMode.Text = ExtractValue(t);
                }
                else if (t.StartsWith("GPU 利用率"))
                {
                    int g = ExtractPercent(t);
                    curGpu = g;
                    SetMetric(valGpu, barGpu, g);
                }
                else if (t.StartsWith("GPU 温度"))
                {
                    double temp = ExtractNumber(t);
                    curTemp = temp;
                    valTemp.Text = temp + " °C";
                    barTemp.Value = (int)Math.Min(100, temp);
                    valTemp.ForeColor = temp >= 85 ? Danger : (temp >= 75 ? Warning : Ink);
                    barTemp.FillColor = temp >= 85 ? Danger : (temp >= 75 ? Warning : Accent);
                }
                else if (t.StartsWith("GPU 功耗"))
                {
                    double power = ExtractNumber(t);
                    curPower = power;
                    valPower.Text = power + " W";
                    barPower.Value = (int)Math.Min(100, power);
                }
                else if (t.StartsWith("显存占用"))
                {
                    double mb = ExtractNumber(t);
                    valVram.Text = string.Format("{0:N0} MB", mb);
                    barVram.Value = (int)Math.Min(100, mb / 81.51);
                }
                else if (t.StartsWith("显存总量"))
                {
                    // 显示总量已有占用值；这里不单独更新
                }
                else if (t.StartsWith("内存占用"))
                {
                    Match m = Regex.Match(t, @"([\d.]+)%\s*\(([\d.]+)\s*GB\s*/\s*([\d.]+)\s*GB\)");
                    if (m.Success)
                    {
                        curMem = double.Parse(m.Groups[1].Value);
                        valMem.Text = m.Groups[1].Value + "%  (" + m.Groups[2].Value + " / " + m.Groups[3].Value + " GB)";
                        barMem.Value = (int)Math.Min(100, (int)curMem);
                    }
                }
                else if (t.StartsWith("CPU 负载"))
                {
                    int c = ExtractPercent(t);
                    curCpu = c;
                    SetMetric(valCpu, barCpu, c);
                }
                else if (t.StartsWith("调度进程数"))
                {
                    int count = (int)ExtractNumber(t);
                    lblScheduler.Text = "调度器: " + (count > 0 ? "运行中" : "未运行");
                    lblScheduler.ForeColor = count > 0 ? Success : Danger;
                }
            }
            if (historyChart != null) historyChart.AddSample(curGpu, curTemp, curPower, curMem, curCpu);
        }

        private string ExtractValue(string line)
        {
            int idx = line.IndexOf(':');
            return idx >= 0 ? line.Substring(idx + 1).Trim() : "";
        }

        private double ExtractNumber(string line)
        {
            Match m = Regex.Match(line, @"([0-9]+(?:\.[0-9]+)?)");
            double v;
            return double.TryParse(m.Groups[1].Value, out v) ? v : 0;
        }

        private int ExtractPercent(string line)
        {
            return (int)ExtractNumber(line);
        }

        private void SetMetric(Label label, PillBar bar, int value)
        {
            label.Text = value + "%";
            bar.Value = Math.Min(100, value);
        }

        private void StartScheduler()
        {
            AppendLog("正在启动智能调度…");
            var p = new Process();
            p.StartInfo.FileName = "powershell.exe";
            p.StartInfo.Arguments = "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File \"" + schedulerPs + "\"";
            p.StartInfo.UseShellExecute = false;
            p.StartInfo.CreateNoWindow = true;
            p.Start();
            AppendLog("[OK] 已后台启动智能调度器");
            RefreshData(true);
        }

        private void StopScheduler()
        {
            AppendLog("正在停止智能调度…");
            RunBatch("schtasks /End /TN GHelperSmartScheduler & schtasks /Change /TN GHelperSmartScheduler /DISABLE");
            string ps = "Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'powershell.exe' -and $_.CommandLine -like '*GHelperSmartScheduler.ps1*' -and $_.ProcessId -ne $PID } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }";
            AppendLog(RunScriptRaw(ps, "-Command"));
            RefreshData(true);
        }

        private void RunScript(string scriptPath, string args)
        {
            string raw = RunScriptRaw(scriptPath, args);
            AppendLog(raw);
            RefreshData(true);
        }

        private string RunScriptRaw(string scriptOrCommand, string args)
        {
            try
            {
                var p = new Process();
                p.StartInfo.FileName = "powershell.exe";
                if (args == "-Command")
                    p.StartInfo.Arguments = "-NoProfile -ExecutionPolicy Bypass -Command \"" + scriptOrCommand + "\"";
                else
                    p.StartInfo.Arguments = "-NoProfile -ExecutionPolicy Bypass -File \"" + scriptOrCommand + "\" " + args;
                p.StartInfo.UseShellExecute = false;
                p.StartInfo.RedirectStandardOutput = true;
                p.StartInfo.RedirectStandardError = true;
                p.StartInfo.CreateNoWindow = true;
                p.Start();
                string output = p.StandardOutput.ReadToEnd();
                string err = p.StandardError.ReadToEnd();
                p.WaitForExit();
                if (!string.IsNullOrEmpty(err)) output += "\n[ERR] " + err;
                return output;
            }
            catch (Exception ex) { return "[EXCEPTION] " + ex.Message; }
        }

        private void RunBatch(string cmdLine)
        {
            try
            {
                var p = new Process();
                p.StartInfo.FileName = "cmd.exe";
                p.StartInfo.Arguments = "/c " + cmdLine;
                p.StartInfo.UseShellExecute = false;
                p.StartInfo.RedirectStandardOutput = true;
                p.StartInfo.RedirectStandardError = true;
                p.StartInfo.CreateNoWindow = true;
                p.Start();
                string output = p.StandardOutput.ReadToEnd();
                string err = p.StandardError.ReadToEnd();
                p.WaitForExit();
                AppendLog(output);
                if (!string.IsNullOrEmpty(err)) AppendLog("[ERR] " + err);
            }
            catch (Exception ex) { AppendLog("[EXCEPTION] " + ex.Message); }
        }

        private void RunMemClean()
        {
            if (!IsAdministrator)
            {
                var r = MessageBox.Show("清理内存需要管理员权限，是否以管理员身份重启本程序？", "权限提示", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
                if (r == DialogResult.Yes) RelaunchElevated();
                return;
            }
            string exe = memReductExe;
            if (!File.Exists(exe)) exe = @"D:\<内存工具目录>\Mem Reduct\memreduct.exe";
            AppendLog("正在调用 Mem Reduct 清理内存…");
            try
            {
                var p = new Process();
                p.StartInfo.FileName = exe;
                p.StartInfo.Arguments = "/clean:0x67";
                p.StartInfo.WorkingDirectory = Path.GetDirectoryName(exe);
                p.StartInfo.UseShellExecute = false;
                p.StartInfo.CreateNoWindow = true;
                p.Start();
                p.WaitForExit();
                AppendLog("[OK] Mem Reduct 已执行清理（/clean:0x67）");
            }
            catch (Exception ex) { AppendLog("[ERR] " + ex.Message); }
        }

        private void OpenDoc()
        {
            try { Process.Start("notepad.exe", @"D:\<工具目录>\优化说明.txt"); }
            catch (Exception ex) { AppendLog("[ERR] 无法打开说明: " + ex.Message); }
        }

        private void RelaunchElevated()
        {
            try
            {
                var psi = new ProcessStartInfo(Application.ExecutablePath);
                psi.Verb = "runas";
                Process.Start(psi);
                Application.Exit();
            }
            catch (Exception ex) { AppendLog("[ERR] 提权失败: " + ex.Message); }
        }

        private void FitToScreen()
        {
            try
            {
                var wa = Screen.PrimaryScreen.WorkingArea;
                if (Width > wa.Width) Width = wa.Width;
                if (Height > wa.Height) Height = wa.Height;
            }
            catch { }
        }

        private void SetupTray()
        {
            notifyIcon = new NotifyIcon();
            notifyIcon.Icon = CreateAppIcon();
            notifyIcon.Text = "NVIDIA 调优";
            notifyIcon.Visible = true;

            var menu = new ContextMenuStrip();
            var open = new ToolStripMenuItem("打开面板");
            open.Click += (s, e) => ShowFromTray();
            var start = new ToolStripMenuItem("启动调度");
            start.Click += (s, e) => StartScheduler();
            var stop = new ToolStripMenuItem("停止调度");
            stop.Click += (s, e) => StopScheduler();
            var refresh = new ToolStripMenuItem("刷新状态");
            refresh.Click += (s, e) => RefreshData(true);
            var exit = new ToolStripMenuItem("退出");
            exit.Click += (s, e) => ExitApp();
            menu.Items.Add(open);
            menu.Items.Add(new ToolStripSeparator());
            menu.Items.Add(start);
            menu.Items.Add(stop);
            menu.Items.Add(refresh);
            menu.Items.Add(new ToolStripSeparator());
            menu.Items.Add(exit);
            notifyIcon.ContextMenuStrip = menu;
            notifyIcon.DoubleClick += (s, e) => ShowFromTray();
            notifyIcon.ShowBalloonTip(2500, "NVIDIA 调优", "已挂后台，双击托盘图标可打开面板", ToolTipIcon.Info);
        }

        private Icon CreateAppIcon()
        {
            Bitmap bmp = new Bitmap(32, 32);
            using (Graphics g = Graphics.FromImage(bmp))
            {
                g.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
                g.Clear(Color.Transparent);
                using (var font = new Font("Segoe MDL2 Assets", 22F, FontStyle.Regular, GraphicsUnit.Pixel))
                using (var brush = new SolidBrush(Accent))
                {
                    var sf = new StringFormat();
                    sf.Alignment = StringAlignment.Center;
                    sf.LineAlignment = StringAlignment.Center;
                    var rect = new RectangleF(0, 0, 32, 32);
                    g.DrawString("\uE7E8", font, brush, rect, sf);
                }
            }
            IntPtr h = bmp.GetHicon();
            return Icon.FromHandle(h);
        }

        private void HideToTray()
        {
            Hide();
            ShowInTaskbar = false;
            notifyIcon.Visible = true;
        }

        private void ShowFromTray()
        {
            Show();
            WindowState = FormWindowState.Normal;
            ShowInTaskbar = true;
            Activate();
        }

        private void ExitApp()
        {
            exitRequested = true;
            notifyIcon.Visible = false;
            Close();
        }

        protected override void OnFormClosing(FormClosingEventArgs e)
        {
            if (!exitRequested)
            {
                e.Cancel = true;
                HideToTray();
                return;
            }
            if (notifyIcon != null) notifyIcon.Dispose();
            base.OnFormClosing(e);
        }

        private void AppendLog(string text)
        {
            if (string.IsNullOrEmpty(text)) return;
            txtLog.AppendText(DateTime.Now.ToString("HH:mm:ss") + "  " + text + Environment.NewLine);
        }

        private bool IsAdministrator
        {
            get
            {
                try
                {
                    var id = System.Security.Principal.WindowsIdentity.GetCurrent();
                    var p = new System.Security.Principal.WindowsPrincipal(id);
                    return p.IsInRole(System.Security.Principal.WindowsBuiltInRole.Administrator);
                }
                catch { return false; }
            }
        }
    }

    static class Program
    {
        [System.Runtime.InteropServices.DllImport("user32.dll")]
        private static extern bool SetProcessDPIAware();

        [STAThread]
        static void Main()
        {
            try { SetProcessDPIAware(); } catch { }
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new MainForm());
        }
    }
}
