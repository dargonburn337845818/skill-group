# 样式速查（可直接抄）

```css
:root {
  --paper:#fffdf8; --ink:#24211f; --ink-65:rgba(36,33,31,.65);
  --ink-45:rgba(36,33,31,.45); --coral:#e97b61; --coral-deep:#d9644e;
  --sage:#c5d8c1; --line:rgba(36,33,31,.16);
  --serif:Georgia,"Times New Roman","Noto Serif SC","Songti SC",serif;
  --sans:"Helvetica Neue",Arial,"PingFang SC","Microsoft YaHei",sans-serif;
}
body{background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.75}
.shell{max-width:720px;margin:0 auto;padding:20px 18px 90px}
.reveal{opacity:0;transform:translateY(14px);transition:opacity .55s ease,transform .55s ease}
.reveal.visible{opacity:1;transform:translateY(0)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{transition-duration:.01ms!important}.reveal{opacity:1!important;transform:none!important}}
```

完整组件根目录：参考 `algorithm-coaching/tier1_pack_stylekit.html` 的 `.masthead/.hero-title/.progress-stick/.toc/.editorial/.panel/.problem/.hint/.recap/.footer`。
