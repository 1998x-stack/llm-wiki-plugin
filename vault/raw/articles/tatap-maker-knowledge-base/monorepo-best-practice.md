# Monorepo 最佳实践：React Native + React Native Web + Vite + Nx

## 🎯 核心建议

**推荐将 Vite + React Web 也放入 Monorepo**

理由：

1. **代码复用最大化**：API 层、业务逻辑、类型定义、工具函数 100% 共享
2. **统一技术栈**：相同的 TypeScript 配置、ESLint、Prettier
3. **原子化部署**：API 更新时，Web 和 Mobile 可以同步适配
4. **开发效率**：一个 PR 跨多端改动，无需跨仓库协调

从 SDK 52 开始，Expo 自动为 monorepo 配置 Metro，不需要手动配置。

---

## 📁 推荐目录结构（Nx-Ready 设计）

这个结构**现在可以作为普通 workspace 使用，将来 5 分钟迁移到 Nx**：

```bash
my-app/                              # 项目根目录
├── apps/                            # 所有应用程序
│   ├── mobile/                      # React Native (Expo) - iOS + Android
│   │   ├── app/                     # Expo Router 路由（文件系统路由）
│   │   │   ├── (tabs)/             # Tab 导航组
│   │   │   │   ├── index.tsx       # 主页
│   │   │   │   ├── profile.tsx     # 个人页
│   │   │   │   └── _layout.tsx     # Tab 布局
│   │   │   ├── (auth)/             # 认证路由组
│   │   │   │   ├── login.tsx
│   │   │   │   └── register.tsx
│   │   │   ├── _layout.tsx         # Root 布局
│   │   │   └── +not-found.tsx      # 404 页面
│   │   ├── assets/                  # 移动端资源
│   │   ├── ios/                     # iOS 原生代码
│   │   ├── android/                 # Android 原生代码
│   │   ├── app.json                 # Expo 配置
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── metro.config.js          # Metro bundler 配置
│   │
│   ├── web/                         # Vite + React 主 Web 应用
│   │   ├── src/
│   │   │   ├── pages/              # 页面组件（与 mobile/app 对应）
│   │   │   │   ├── Home.tsx
│   │   │   │   ├── Profile.tsx
│   │   │   │   └── Login.tsx
│   │   │   ├── App.tsx
│   │   │   ├── main.tsx
│   │   │   └── router.tsx          # React Router 配置
│   │   ├── public/
│   │   ├── index.html
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── vite.config.ts
│   │
│   ├── web-landing/                 # 营销落地页（可选，独立部署）
│   │   ├── src/
│   │   ├── package.json
│   │   └── vite.config.ts
│   │
│   ├── server-api/                  # 主 API 服务器（Node.js/Express）
│   │   ├── src/
│   │   │   ├── routes/
│   │   │   ├── controllers/
│   │   │   ├── middleware/
│   │   │   ├── services/
│   │   │   └── index.ts
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   ├── server-ws/                   # WebSocket 服务器（实时通信）
│   │   ├── src/
│   │   │   ├── handlers/
│   │   │   └── index.ts
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   └── server-worker/               # 后台任务处理（可选，如 BullMQ）
│       ├── src/
│       ├── package.json
│       └── tsconfig.json
│
├── packages/                        # 共享代码包
│   ├── ui/                          # 跨平台 UI 组件库（核心）
│   │   ├── src/
│   │   │   ├── Button/
│   │   │   │   ├── Button.tsx      # 使用 RN 原语
│   │   │   │   ├── Button.web.tsx  # Web 特定优化（可选）
│   │   │   │   └── index.ts
│   │   │   ├── Input/
│   │   │   ├── Card/
│   │   │   ├── Modal/
│   │   │   └── index.ts            # 统一导出
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   ├── api-client/                  # API 客户端（Axios/Fetch 封装）
│   │   ├── src/
│   │   │   ├── client.ts           # 基础 HTTP 客户端
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.ts         # /auth/* 接口
│   │   │   │   ├── user.ts         # /user/* 接口
│   │   │   │   └── post.ts         # /post/* 接口
│   │   │   └── index.ts
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   ├── shared/                      # 通用共享代码
│   │   ├── src/
│   │   │   ├── utils/              # 工具函数
│   │   │   │   ├── format.ts
│   │   │   │   ├── validate.ts
│   │   │   │   └── storage.ts
│   │   │   ├── constants/          # 常量
│   │   │   │   ├── config.ts
│   │   │   │   └── routes.ts
│   │   │   ├── hooks/              # 通用 React hooks
│   │   │   │   ├── useAuth.ts
│   │   │   │   └── useDebounce.ts
│   │   │   └── helpers/            # 业务逻辑辅助
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   ├── types/                       # TypeScript 类型定义
│   │   ├── src/
│   │   │   ├── api/                # API 类型
│   │   │   │   ├── user.ts
│   │   │   │   └── post.ts
│   │   │   ├── models/             # 数据模型
│   │   │   │   ├── User.ts
│   │   │   │   └── Post.ts
│   │   │   └── index.ts
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   ├── features/                    # 功能模块（按业务领域）
│   │   ├── auth/                   # 认证功能
│   │   │   ├── src/
│   │   │   │   ├── api.ts          # 认证相关 API
│   │   │   │   ├── hooks.ts        # 认证 hooks
│   │   │   │   ├── store.ts        # 认证状态（Zustand）
│   │   │   │   └── components/     # 认证相关组件
│   │   │   │       ├── LoginForm.tsx
│   │   │   │       └── AuthGuard.tsx
│   │   │   ├── package.json
│   │   │   └── tsconfig.json
│   │   │
│   │   ├── chat/                   # 聊天功能
│   │   │   ├── src/
│   │   │   │   ├── api.ts
│   │   │   │   ├── hooks.ts
│   │   │   │   ├── store.ts
│   │   │   │   └── components/
│   │   │   ├── package.json
│   │   │   └── tsconfig.json
│   │   │
│   │   └── profile/                # 个人资料功能
│   │       ├── src/
│   │       ├── package.json
│   │       └── tsconfig.json
│   │
│   └── config/                      # 配置共享
│       ├── eslint-config/          # ESLint 配置
│       │   ├── index.js
│       │   └── package.json
│       ├── typescript-config/      # TypeScript 配置
│       │   ├── base.json
│       │   ├── react.json
│       │   ├── node.json
│       │   └── package.json
│       └── jest-config/            # Jest 配置
│           ├── base.js
│           └── package.json
│
├── tools/                           # 开发工具和脚本
│   ├── scripts/
│   │   ├── generate-icons.sh       # 生成应用图标
│   │   └── sync-env.sh             # 同步环境变量
│   └── generators/                 # 代码生成器（可选）
│
├── .github/                         # GitHub 配置
│   └── workflows/
│       ├── ci.yml                  # CI/CD 配置
│       └── release.yml
│
├── docs/                            # 项目文档
│   ├── architecture.md
│   ├── api.md
│   └── deployment.md
│
├── package.json                     # Root workspace 配置
├── pnpm-workspace.yaml             # pnpm workspace 配置（推荐）
├── turbo.json                      # Turborepo 配置（可选，暂时不用）
├── nx.json                         # Nx 配置（将来迁移时添加）
├── tsconfig.base.json              # Base TypeScript 配置
├── .eslintrc.js                    # Root ESLint 配置
├── .prettierrc                     # Prettier 配置
├── .gitignore
└── README.md
```

---

## 🔧 初始化步骤（不使用 Nx）

### **1. 创建 workspace（使用 pnpm，推荐）**

```bash
# 创建项目目录
mkdir my-app && cd my-app

# 初始化 root package.json
pnpm init

# 创建 workspace 配置
cat > pnpm-workspace.yaml << EOF
packages:
  - 'apps/*'
  - 'packages/*'
EOF
```

### **2. 配置 Root package.json**

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev:mobile": "pnpm --filter mobile dev",
    "dev:web": "pnpm --filter web dev",
    "dev:api": "pnpm --filter server-api dev",
    "build:all": "pnpm -r build",
    "test": "pnpm -r test",
    "lint": "pnpm -r lint",
    "type-check": "pnpm -r type-check"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.3.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0"
  }
}
```

### **3. 创建 Mobile 应用（Expo Router）**

```bash
# 在 apps 目录下
cd apps
npx create-expo-app mobile --template tabs
cd mobile

# 安装 Expo Router
npx expo install expo-router react-native-safe-area-context react-native-screens

# 配置 package.json
```

**apps/mobile/package.json**：

```json
{
  "name": "mobile",
  "version": "1.0.0",
  "main": "expo-router/entry",
  "scripts": {
    "start": "expo start",
    "dev": "expo start",
    "ios": "expo start --ios",
    "android": "expo start --android",
    "web": "expo start --web"
  },
  "dependencies": {
    "expo": "~52.0.0",
    "expo-router": "~4.0.0",
    "react": "19.1.0",
    "react-native": "0.81.1",
    "@my-app/ui": "workspace:*",
    "@my-app/api-client": "workspace:*",
    "@my-app/shared": "workspace:*",
    "@my-app/types": "workspace:*",
    "@my-app/features-auth": "workspace:*"
  }
}
```

**apps/mobile/metro.config.js**：

```javascript
const { getDefaultConfig } = require("expo/metro-config");
const path = require("path");

const projectRoot = __dirname;
const workspaceRoot = path.resolve(projectRoot, "../..");

const config = getDefaultConfig(projectRoot);

// Expo SDK 52+ 自动处理 monorepo，但我们明确配置以保证兼容性
config.watchFolders = [workspaceRoot];
config.resolver.nodeModulesPaths = [
  path.resolve(projectRoot, "node_modules"),
  path.resolve(workspaceRoot, "node_modules"),
];

module.exports = config;
```

### **4. 创建 Web 应用（Vite + React）**

```bash
cd apps
pnpm create vite web --template react-ts
cd web
```

**apps/web/package.json**：

```json
{
  "name": "web",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^6.0.0",
    "@my-app/ui": "workspace:*",
    "@my-app/api-client": "workspace:*",
    "@my-app/shared": "workspace:*",
    "@my-app/types": "workspace:*",
    "@my-app/features-auth": "workspace:*"
  },
  "devDependencies": {
    "vite": "^6.0.0",
    "@vitejs/plugin-react": "^4.0.0"
  }
}
```

**apps/web/vite.config.ts**：

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "react-native": "react-native-web",
      // 允许直接导入 packages
      "@my-app/ui": path.resolve(__dirname, "../../packages/ui/src"),
      "@my-app/shared": path.resolve(__dirname, "../../packages/shared/src"),
    },
  },
  optimizeDeps: {
    include: ["react-native-web"],
  },
});
```

### **5. 创建 API 服务器**

```bash
cd apps
mkdir server-api && cd server-api
pnpm init
```

**apps/server-api/package.json**：

```json
{
  "name": "server-api",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js"
  },
  "dependencies": {
    "express": "^4.18.0",
    "cors": "^2.8.5",
    "@my-app/types": "workspace:*",
    "@my-app/shared": "workspace:*"
  },
  "devDependencies": {
    "@types/express": "^4.17.0",
    "@types/cors": "^2.8.0",
    "tsx": "^4.0.0",
    "typescript": "^5.3.0"
  }
}
```

### **6. 创建共享 UI 包**

```bash
cd packages
mkdir ui && cd ui
pnpm init
```

**packages/ui/package.json**：

```json
{
  "name": "@my-app/ui",
  "version": "1.0.0",
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "scripts": {
    "type-check": "tsc --noEmit"
  },
  "peerDependencies": {
    "react": ">=18.0.0",
    "react-native": ">=0.70.0"
  },
  "dependencies": {
    "@my-app/types": "workspace:*"
  },
  "devDependencies": {
    "@types/react": "^18.0.0",
    "typescript": "^5.3.0"
  }
}
```

**packages/ui/src/Button/Button.tsx**（示例）：

```typescript
import { Pressable, Text, StyleSheet, Platform } from 'react-native';
import type { ButtonProps } from '@my-app/types';

export const Button = ({ title, onPress, variant = 'primary' }: ButtonProps) => {
  return (
    <Pressable
      style={[
        styles.base,
        styles[variant],
        Platform.select({
          web: styles.web,
          ios: styles.ios,
        })
      ]}
      onPress={onPress}
    >
      <Text style={styles.text}>{title}</Text>
    </Pressable>
  );
};

const styles = StyleSheet.create({
  base: {
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    alignItems: 'center',
  },
  primary: {
    backgroundColor: '#007AFF',
  },
  secondary: {
    backgroundColor: '#8E8E93',
  },
  web: {
    cursor: 'pointer',
    userSelect: 'none',
  },
  ios: {
    shadowColor: '#000',
    shadowOpacity: 0.1,
  },
  text: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
```

### **7. Base TypeScript 配置**

**tsconfig.base.json**（root）：

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "resolveJsonModule": true,
    "allowJs": true,
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "baseUrl": ".",
    "paths": {
      "@my-app/ui": ["packages/ui/src"],
      "@my-app/api-client": ["packages/api-client/src"],
      "@my-app/shared": ["packages/shared/src"],
      "@my-app/types": ["packages/types/src"],
      "@my-app/features-*": ["packages/features/*/src"]
    }
  }
}
```

---

## 🚀 将来迁移到 Nx（5 分钟搞定）

当项目规模增长，需要更好的任务编排和缓存时：

```bash
# 1. 安装 Nx
pnpm add -D nx @nx/workspace

# 2. 初始化 Nx
npx nx init

# 3. Nx 自动检测 workspace 结构，无需改动目录！

# 4. 使用 Nx 运行任务
nx run mobile:start
nx run web:dev
nx run server-api:build

# 5. 并行构建所有项目
nx run-many -t build --all

# 6. 只构建变更的项目
nx affected -t build
```

Nx 会自动生成 `nx.json` 和 `project.json` 配置，检测你的 apps 和 packages 结构。

---

## 💡 关键设计原则

### **1. 命名约定（现在就固定）**

```typescript
// Package 命名规则
@my-app/ui              // UI 组件库
@my-app/api-client      // API 客户端
@my-app/types           // 类型定义
@my-app/shared          // 通用工具
@my-app/features-auth   // 功能模块（auth）
@my-app/features-chat   // 功能模块（chat）

// Import 示例
import { Button } from '@my-app/ui';
import { useAuth } from '@my-app/features-auth';
import type { User } from '@my-app/types';
```

### **2. 依赖规则**

```
应用层（apps/*）      → 可以依赖任何 packages
功能模块（features/*） → 可以依赖 ui、shared、types、api-client
UI 组件（ui）         → 只能依赖 types
工具库（shared）      → 只能依赖 types
类型定义（types）     → 不依赖任何包（最底层）
```

### **3. 环境变量管理**

```bash
# Root .env.example
DATABASE_URL=
API_URL=https://api.example.com
WS_URL=wss://ws.example.com

# apps/mobile/.env
EXPO_PUBLIC_API_URL=https://api.example.com

# apps/web/.env
VITE_API_URL=https://api.example.com

# apps/server-api/.env
PORT=3000
DATABASE_URL=postgresql://...
```

---

## ⚠️ 注意事项与最佳实践

### **1. React Native Web 兼容性**

```typescript
// ✅ 好的做法：使用 RN 原语
import { View, Text, Pressable } from "react-native";

// ❌ 避免：直接使用 DOM 元素
// import { div, button } from 'react';
```

### **2. Platform-specific 代码**

```typescript
// Button.tsx（共享）
export { Button } from "./Button.native";

// Button.web.tsx（Web 优化版本）
export const Button = (props) => {
  // Web-specific implementation
};

// Metro 和 Vite 会自动选择正确的文件
```

### **3. 避免循环依赖**

```bash
# 检查循环依赖
npx madge --circular --extensions ts,tsx packages/*/src
```

### **4. 版本同步**

确保 React 和 React Native 版本在整个 monorepo 中保持一致，避免重复安装导致的运行时错误。

---

## 📊 与其他方案对比

| 特性     | 这个方案         | 纯 Turborepo | 纯 Nx             |
| -------- | ---------------- | ------------ | ----------------- |
| 学习曲线 | ⭐⭐ 简单        | ⭐⭐ 简单    | ⭐⭐⭐ 中等       |
| 初始设置 | ⭐⭐⭐⭐⭐ 快    | ⭐⭐⭐⭐ 快  | ⭐⭐⭐ 中等       |
| 可扩展性 | ⭐⭐⭐⭐⭐ 优秀  | ⭐⭐⭐⭐ 好  | ⭐⭐⭐⭐⭐ 优秀   |
| 迁移成本 | 无（已做好准备） | 中等         | 无                |
| 工具支持 | 标准 workspace   | Turborepo    | Nx Console + 插件 |

---

## 🎯 总结与建议

**这个目录结构的优势：**

1. ✅ **现在就能用**：标准 pnpm workspace，无需 Nx
2. ✅ **5 分钟迁移到 Nx**：结构完全兼容
3. ✅ **清晰的边界**：apps vs packages 分离
4. ✅ **按功能模块化**：features/\* 易于团队协作
5. ✅ **多服务器支持**：API、WebSocket、Worker 独立部署
6. ✅ **统一代码风格**：共享 ESLint、TypeScript 配置

**[判断与建议]**

- **现阶段（< 50K LOC）**：使用 pnpm workspace + 上述结构，足够轻量
- **中期（50-200K LOC）**：加入 Turborepo 用于缓存和并行构建
- **大型项目（> 200K LOC）**：迁移到 Nx，获得更高级的功能

**今天就可以开始**，未来无需重构目录结构！🚀

## 问题 1：为什么推荐 pnpm？

### **核心对比表（2025 年数据）**

| 特性                    | pnpm                                   | Yarn (Classic/Berry) | Bun                         |
| ----------------------- | -------------------------------------- | -------------------- | --------------------------- |
| **安装速度**            | ⭐⭐⭐⭐ 快                            | ⭐⭐⭐ 中等          | ⭐⭐⭐⭐⭐ 最快             |
| **磁盘效率**            | ⭐⭐⭐⭐⭐ 比 npm/Yarn 节省 70% 空间   | ⭐⭐ 占用大          | ⭐⭐⭐⭐ 好                 |
| **Monorepo 支持**       | ⭐⭐⭐⭐⭐ 优秀的 workspace 过滤和管理 | ⭐⭐⭐⭐ 好          | ⭐⭐⭐ 2025 年改进中        |
| **生态成熟度**          | ⭐⭐⭐⭐⭐ 成熟                        | ⭐⭐⭐⭐⭐ 成熟      | ⭐⭐⭐ 新工具，社区还在成长 |
| **React Native 兼容性** | ⭐⭐⭐⭐⭐ 完美                        | ⭐⭐⭐⭐ 好          | ⭐⭐⭐ 部分包可能有问题     |
| **学习曲线**            | ⭐⭐⭐⭐ 易学                          | ⭐⭐⭐ 中等          | ⭐⭐⭐⭐ 易学               |

### **pnpm 的独特优势（为什么适合你的场景）**

#### **1. 严格的依赖管理**

pnpm 强制执行严格的依赖声明，防止意外访问未声明的包：

```bash
# 情景：你在 apps/mobile 中不小心用了没声明的 lodash

# ❌ npm/yarn：能正常运行（因为 hoisting，其他包安装了）
import { debounce } from 'lodash'; // 能用！

# ✅ pnpm：立即报错
Module not found: Can't resolve 'lodash'
# 必须显式声明：pnpm add lodash
```

这对 **Monorepo 至关重要**——避免隐藏的依赖关系。

#### **2. 磁盘空间节省（对大项目显著）**

```bash
# 假设你有 5 个项目都用 React 18.2.0

# npm/yarn:
~/projects/app1/node_modules/react  (500KB)
~/projects/app2/node_modules/react  (500KB)
~/projects/app3/node_modules/react  (500KB)
# 总计：2.5MB

# pnpm:
~/.pnpm-store/react@18.2.0/         (500KB)
~/projects/app1/.pnpm/react -> symlink
~/projects/app2/.pnpm/react -> symlink
# 总计：500KB + 微小的 symlink
```

#### **3. Monorepo Workspace 过滤（超强）**

pnpm 的 workspace 命令包含强大的过滤功能：

```bash
# 只为特定包安装依赖
pnpm --filter mobile add react-native-reanimated

# 运行所有依赖某个包的项目测试
pnpm --filter "...@my-app/ui" run test

# 并行构建所有 apps
pnpm -r --filter "./apps/**" build

# 运行变更影响的包（类似 Nx affected）
pnpm --filter "...[origin/main]" build
```

#### **4. React Native 兼容性最佳**

```bash
# pnpm 对 React Native 的特殊处理
# .npmrc 配置
node-linker=hoisted  # RN 需要 hoisted
public-hoist-pattern[]=*react-native*
public-hoist-pattern[]=*expo*
```

---

### **为什么不推荐其他的？**

#### **Yarn (Classic v1.x)** ❌

- 已停止维护（2020 年后）
- 磁盘占用大
- 比 pnpm 慢

#### **Yarn Berry (v2+/v4+)** ⚠️

- Plug'n'Play (PnP) 模式与 React Native **不兼容**
- 需要额外配置才能用 `node_modules`
- 学习曲线陡峭

#### **Bun** ⚠️

虽然 Bun 是最快的（安装速度比 npm 快 20-30 倍），但它仍在成熟中：

- 社区和生态系统还在初期阶段
- 某些 npm 包可能不完全兼容
- React Native 支持还不够完善（2025 年）
- **适合新项目原型**，不适合生产级 Monorepo

---

### **性能对比（实测数据）**

在 ~350 个包的 Node.js 库测试（干净克隆）：

- **Bun install**: 3.4 秒
- **pnpm**: 12.1 秒
- **npm**: 19.6 秒
- **Yarn**: 49.2 秒

**但速度不是唯一考虑因素**——你需要：

- ✅ 稳定性
- ✅ React Native 兼容性
- ✅ Monorepo 工具成熟度
- ✅ 社区支持

**结论：pnpm 在所有维度平衡最好**。

---

## 问题 2：shadcn/ui 在 Monorepo 中的配置

### **官方支持，完全可行！✅**

shadcn/ui 官方提供 Monorepo 支持，你的目录结构**完全正确**：

```bash
packages/ui/src/              # ✅ shadcn/ui 组件放这里
apps/web/                     # ✅ Vite 应用在这里
```

### **完整配置步骤**

#### **1. 初始化 shadcn/ui（推荐方式）**

在项目根目录运行：

```bash
cd my-app  # 项目根目录
pnpm dlx shadcn@canary init

# 选择 Monorepo 选项
? Select a framework › React
? Would you like to use TypeScript? › Yes
? Where is your global CSS file? › packages/ui/src/styles/globals.css
? Where is your tailwind.config located? › packages/ui/tailwind.config.ts
? Configure the import alias for components: › @my-app/ui/components
? Configure the import alias for utils: › @my-app/ui/lib/utils
```

#### **2. 目录结构（最终效果）**

```bash
my-app/
├── apps/
│   └── web/
│       ├── src/
│       │   ├── App.tsx              # 使用 UI 组件
│       │   └── main.tsx
│       ├── components.json          # shadcn 配置（指向 packages/ui）
│       ├── vite.config.ts
│       └── package.json
│
├── packages/
│   └── ui/
│       ├── src/
│       │   ├── components/          # shadcn/ui 组件在这里！
│       │   │   ├── ui/             # shadcn 自动生成
│       │   │   │   ├── button.tsx
│       │   │   │   ├── card.tsx
│       │   │   │   └── input.tsx
│       │   │   └── custom/         # 你自己的组件
│       │   ├── lib/
│       │   │   └── utils.ts        # cn() 工具函数
│       │   ├── styles/
│       │   │   └── globals.css     # Tailwind CSS
│       │   └── index.ts            # 统一导出
│       ├── components.json          # UI 包的 shadcn 配置
│       ├── tailwind.config.ts      # Tailwind 配置
│       ├── tsconfig.json
│       └── package.json
```

#### **3. packages/ui/components.json 配置**

这是关键文件，告诉 shadcn CLI 如何安装组件：

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "src/styles/globals.css",
    "baseColor": "zinc",
    "cssVariables": true
  },
  "aliases": {
    "components": "@my-app/ui/components",
    "utils": "@my-app/ui/lib/utils",
    "ui": "@my-app/ui/components/ui",
    "lib": "@my-app/ui/lib"
  }
}
```

#### **4. apps/web/components.json 配置**

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "../../packages/ui/tailwind.config.ts",
    "css": "../../packages/ui/src/styles/globals.css",
    "baseColor": "zinc",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@my-app/ui/lib/utils",
    "ui": "@my-app/ui/components/ui"
  }
}
```

#### **5. packages/ui/package.json**

```json
{
  "name": "@my-app/ui",
  "version": "1.0.0",
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": {
    "./components/*": "./src/components/*.tsx",
    "./lib/*": "./src/lib/*.ts",
    "./styles/*": "./src/styles/*.css"
  },
  "dependencies": {
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0",
    "@radix-ui/react-slot": "^1.0.0"
  },
  "peerDependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "tailwindcss": "^4.0.0",
    "typescript": "^5.0.0"
  }
}
```

#### **6. packages/ui/tailwind.config.ts**

```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/**/*.{ts,tsx}",
    "../../apps/web/src/**/*.{ts,tsx}", // 扫描 web app
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        // ... shadcn 的 CSS 变量
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
```

#### **7. apps/web/vite.config.ts（关键配置）**

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      // 应用自己的别名
      "@": path.resolve(__dirname, "./src"),

      // 指向 UI 包的别名（与 components.json 一致）
      "@my-app/ui": path.resolve(__dirname, "../../packages/ui/src"),
    },
  },
  css: {
    postcss: path.resolve(__dirname, "../../packages/ui/postcss.config.js"),
  },
});
```

#### **8. apps/web/src/main.tsx（导入全局样式）**

```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// ✅ 导入 UI 包的全局样式（包含 Tailwind + shadcn 变量）
import '@my-app/ui/styles/globals.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
```

---

### **使用方式**

#### **添加新组件**

在 apps/web 目录下运行：

```bash
# 方法 1：从 web 应用目录运行
cd apps/web
pnpm dlx shadcn@latest add button

# 方法 2：从根目录指定配置文件
pnpm dlx shadcn@latest add button -c apps/web

# ✅ 结果：
# - 组件安装到 packages/ui/src/components/ui/button.tsx
# - 依赖自动添加到 packages/ui/package.json
# - 可以立即在 apps/web 中使用
```

#### **在应用中使用**

```typescript
// apps/web/src/App.tsx
import { Button } from '@my-app/ui/components/ui/button';
import { Card, CardHeader, CardContent } from '@my-app/ui/components/ui/card';

function App() {
  return (
    <Card>
      <CardHeader>Hello Monorepo</CardHeader>
      <CardContent>
        <Button variant="default">Click Me</Button>
      </CardContent>
    </Card>
  );
}
```

---

### **常见问题解决**

#### **问题 1：Tailwind 样式不生效**

```typescript
// ❌ 错误：packages/ui/tailwind.config.ts 没扫描 web app
content: ["./src/**/*.{ts,tsx}"];

// ✅ 正确：扫描所有使用 UI 组件的应用
content: [
  "./src/**/*.{ts,tsx}",
  "../../apps/web/src/**/*.{ts,tsx}",
  "../../apps/mobile/app/**/*.{ts,tsx}", // 如果 mobile 也用
];
```

#### **问题 2：模块找不到**

```bash
# 确保 workspace 依赖正确声明
cd apps/web
pnpm add @my-app/ui@workspace:*

# 然后重启 Vite dev server
pnpm dev
```

#### **问题 3：CSS 变量未定义**

确保 `packages/ui/src/styles/globals.css` 包含所有 shadcn 的 CSS 变量：

```css
/* packages/ui/src/styles/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    /* ... 完整变量列表见 shadcn 文档 */
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    /* ... */
  }
}
```

---

## 🎯 总结

### **问题 1 答案：**

**推荐 pnpm** 因为：

1. 在 Monorepo 中性能和磁盘效率最佳
2. 严格的依赖管理防止隐藏问题
3. React Native 兼容性好
4. 工具链成熟稳定

**Bun 虽然最快，但 2025 年还不够成熟用于生产**。

### **问题 2 答案：**

**完全支持！** shadcn/ui 官方提供 Monorepo 模式：

- ✅ 组件放在 `packages/ui/src/components`
- ✅ Vite app 在 `apps/web`
- ✅ 通过 `components.json` 配置路径映射
- ✅ 一次添加，所有应用共享

参考现成项目：shadcn-vite-react-typescript-monorepo

**[判断与建议]** 你的目录结构设计**完全正确**，shadcn/ui + Vite + pnpm 是 2025 年的最佳实践组合！🚀
