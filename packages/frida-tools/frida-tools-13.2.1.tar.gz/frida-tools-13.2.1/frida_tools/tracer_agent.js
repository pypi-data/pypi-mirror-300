(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
(function (global){(function (){
"use strict";

var e, t = this && this.__classPrivateFieldGet || function(e, t, s, n) {
  if ("a" === s && !n) throw new TypeError("Private accessor was defined without a getter");
  if ("function" == typeof t ? e !== t || !n : !t.has(e)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
  return "m" === s ? n : "a" === s ? n.call(e) : n ? n.value : t.get(e);
}, s = this && this.__classPrivateFieldSet || function(e, t, s, n, r) {
  if ("m" === n) throw new TypeError("Private method is not writable");
  if ("a" === n && !r) throw new TypeError("Private accessor was defined without a setter");
  if ("function" == typeof t ? e !== t || !r : !t.has(e)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
  return "a" === n ? r.call(e, s) : r ? r.value = s : t.set(e, s), s;
};

const n = 1e3;

class r {
  constructor() {
    this.handlers = new Map, this.nativeTargets = new Set, this.stagedPlanRequest = null, 
    this.stackDepth = new Map, this.traceState = {}, this.nextId = 1, this.started = Date.now(), 
    this.pendingEvents = [], this.flushTimer = null, this.cachedModuleResolver = null, 
    this.cachedObjcResolver = null, this.cachedSwiftResolver = null, this.onTraceError = ({id: e, name: t, message: s}) => {
      send({
        type: "agent:warning",
        id: e,
        message: `Skipping "${t}": ${s}`
      });
    }, this.flush = () => {
      if (null !== this.flushTimer && (clearTimeout(this.flushTimer), this.flushTimer = null), 
      0 === this.pendingEvents.length) return;
      const e = this.pendingEvents;
      this.pendingEvents = [], send({
        type: "events:add",
        events: e
      });
    };
  }
  init(e, t, s, n) {
    const r = global;
    r.stage = e, r.parameters = t, r.state = this.traceState, r.defineHandler = e => e;
    for (const e of s) try {
      (0, eval)(e.source);
    } catch (t) {
      throw new Error(`unable to load ${e.filename}: ${t.stack}`);
    }
    return this.start(n).catch((e => {
      send({
        type: "agent:error",
        message: e.message
      });
    })), {
      id: Process.id,
      platform: Process.platform,
      arch: Process.arch,
      pointer_size: Process.pointerSize,
      page_size: Process.pageSize,
      main_module: Process.mainModule
    };
  }
  dispose() {
    this.flush();
  }
  updateHandlerCode(e, t, s) {
    const n = this.handlers.get(e);
    if (void 0 === n) throw new Error("invalid target ID");
    if (3 === n.length) {
      const r = this.parseFunctionHandler(s, e, t, this.onTraceError);
      n[0] = r[0], n[1] = r[1];
    } else {
      const r = this.parseInstructionHandler(s, e, t, this.onTraceError);
      n[0] = r[0];
    }
  }
  updateHandlerConfig(e, t) {
    const s = this.handlers.get(e);
    if (void 0 === s) throw new Error("invalid target ID");
    s[2] = t;
  }
  async stageTargets(e) {
    const t = await this.createPlan(e);
    this.stagedPlanRequest = t, await t.ready;
    const {plan: s} = t, n = [];
    let r = 1;
    for (const [e, t, a] of s.native.values()) n.push([ r, t, a ]), r++;
    r = -1;
    for (const e of s.java) for (const [t, s] of e.classes.entries()) for (const e of s.methods.values()) n.push([ r, t, e ]), 
    r--;
    return n;
  }
  async commitTargets(e) {
    const t = this.stagedPlanRequest;
    this.stagedPlanRequest = null;
    let {plan: s} = t;
    null !== e && (s = this.cropStagedPlan(s, e));
    const n = [], r = e => {
      n.push(e);
    }, a = await this.traceNativeTargets(s.native, r);
    let o = [];
    return 0 !== s.java.length && (o = await new Promise(((e, t) => {
      Java.perform((() => {
        this.traceJavaTargets(s.java, r).then(e, t);
      }));
    }))), {
      ids: [ ...a, ...o ],
      errors: n
    };
  }
  readMemory(e, t) {
    try {
      return ptr(e).readByteArray(t);
    } catch (e) {
      return null;
    }
  }
  resolveAddresses(e) {
    let t = null;
    return e.map(ptr).map(DebugSymbol.fromAddress).map((e => {
      if (null === e.name) {
        null === t && (t = new ModuleMap);
        const s = t.find(e.address);
        if (null !== s) return `${s.name}!${e.address.sub(s.base)}`;
      }
      return e;
    })).map((e => e.toString()));
  }
  cropStagedPlan(e, t) {
    let s;
    if (t < 0) {
      s = -1;
      for (const n of e.java) for (const [e, r] of n.classes.entries()) for (const [a, o] of r.methods.entries()) {
        if (s === t) {
          const t = {
            methods: new Map([ [ a, o ] ])
          }, s = {
            loader: n.loader,
            classes: new Map([ [ e, t ] ])
          }, r = new b;
          return r.java.push(s), r;
        }
        s--;
      }
    } else {
      s = 1;
      for (const [n, r] of e.native.entries()) {
        if (s === t) {
          const e = new b;
          return e.native.set(n, r), e;
        }
        s++;
      }
    }
    throw new Error("invalid staged item ID");
  }
  async start(e) {
    const t = await this.createPlan(e, (async e => {
      await this.traceJavaTargets(e.java, this.onTraceError);
    }));
    await this.traceNativeTargets(t.plan.native, this.onTraceError), send({
      type: "agent:initialized"
    }), t.ready.then((() => {
      send({
        type: "agent:started",
        count: this.handlers.size
      });
    }));
  }
  async createPlan(e, t = async () => {}) {
    const s = new b, n = [];
    for (const [t, r, a] of e) switch (r) {
     case "module":
      "include" === t ? this.includeModule(a, s) : this.excludeModule(a, s);
      break;

     case "function":
      "include" === t ? this.includeFunction(a, s) : this.excludeFunction(a, s);
      break;

     case "relative-function":
      "include" === t && this.includeRelativeFunction(a, s);
      break;

     case "absolute-instruction":
      "include" === t && this.includeAbsoluteInstruction(ptr(a), s);
      break;

     case "imports":
      "include" === t && this.includeImports(a, s);
      break;

     case "objc-method":
      "include" === t ? this.includeObjCMethod(a, s) : this.excludeObjCMethod(a, s);
      break;

     case "swift-func":
      "include" === t ? this.includeSwiftFunc(a, s) : this.excludeSwiftFunc(a, s);
      break;

     case "java-method":
      n.push([ t, a ]);
      break;

     case "debug-symbol":
      "include" === t && this.includeDebugSymbol(a, s);
    }
    for (const e of s.native.keys()) this.nativeTargets.has(e) && s.native.delete(e);
    let r, a = !0;
    if (n.length > 0) {
      if (!Java.available) throw new Error("Java runtime is not available");
      r = new Promise(((e, r) => {
        Java.perform((async () => {
          a = !1;
          try {
            for (const [e, t] of n) "include" === e ? this.includeJavaMethod(t, s) : this.excludeJavaMethod(t, s);
            await t(s), e();
          } catch (e) {
            r(e);
          }
        }));
      }));
    } else r = Promise.resolve();
    return a || await r, {
      plan: s,
      ready: r
    };
  }
  async traceNativeTargets(e, t) {
    const s = new Map, n = new Map, r = new Map, a = new Map;
    for (const [t, [o, i, c]] of e.entries()) {
      let e;
      switch (o) {
       case "insn":
        e = s;
        break;

       case "c":
        e = n;
        break;

       case "objc":
        e = r;
        break;

       case "swift":
        e = a;
      }
      let l = e.get(i);
      void 0 === l && (l = [], e.set(i, l)), l.push([ c, ptr(t) ]);
    }
    const [o, i, c] = await Promise.all([ this.traceNativeEntries("insn", s, t), this.traceNativeEntries("c", n, t), this.traceNativeEntries("objc", r, t), this.traceNativeEntries("swift", a, t) ]);
    return [ ...o, ...i, ...c ];
  }
  async traceNativeEntries(e, t, s) {
    if (0 === t.size) return [];
    const n = this.nextId, r = [], o = {
      type: "handlers:get",
      flavor: e,
      baseId: n,
      scopes: r
    };
    for (const [e, s] of t.entries()) r.push({
      name: e,
      members: s.map((e => e[0])),
      addresses: s.map((e => e[1].toString()))
    }), this.nextId += s.length;
    const {scripts: i} = await a(o), c = [];
    let l = 0;
    const d = "insn" === e;
    for (const e of t.values()) for (const [t, r] of e) {
      const e = n + l, a = "string" == typeof t ? t : t[1], o = d ? this.parseInstructionHandler(i[l], e, a, s) : this.parseFunctionHandler(i[l], e, a, s);
      this.handlers.set(e, o), this.nativeTargets.add(r.toString());
      try {
        Interceptor.attach(r, d ? this.makeNativeInstructionListener(e, o) : this.makeNativeFunctionListener(e, o));
      } catch (t) {
        s({
          id: e,
          name: a,
          message: t.message
        });
      }
      c.push(e), l++;
    }
    return c;
  }
  async traceJavaTargets(e, t) {
    const s = this.nextId, n = [], r = {
      type: "handlers:get",
      flavor: "java",
      baseId: s,
      scopes: n
    };
    for (const t of e) for (const [e, {methods: s}] of t.classes.entries()) {
      const t = e.split("."), r = t[t.length - 1], a = Array.from(s.keys()).map((e => [ e, `${r}.${e}` ]));
      n.push({
        name: e,
        members: a
      }), this.nextId += a.length;
    }
    const {scripts: o} = await a(r);
    return new Promise((n => {
      Java.perform((() => {
        const r = [];
        let a = 0;
        for (const n of e) {
          const e = Java.ClassFactory.get(n.loader);
          for (const [i, {methods: c}] of n.classes.entries()) {
            const n = e.use(i);
            for (const [e, i] of c.entries()) {
              const c = s + a, l = this.parseFunctionHandler(o[a], c, i, t);
              this.handlers.set(c, l);
              const d = n[e];
              for (const e of d.overloads) e.implementation = this.makeJavaMethodWrapper(c, e, l);
              r.push(c), a++;
            }
          }
        }
        n(r);
      }));
    }));
  }
  makeNativeFunctionListener(e, t) {
    const s = this;
    return {
      onEnter(n) {
        const [r, a, o] = t;
        s.invokeNativeHandler(e, r, o, this, n, ">");
      },
      onLeave(n) {
        const [r, a, o] = t;
        s.invokeNativeHandler(e, a, o, this, n, "<");
      }
    };
  }
  makeNativeInstructionListener(e, t) {
    const s = this;
    return function(n) {
      const [r, a] = t;
      s.invokeNativeHandler(e, r, a, this, n, "|");
    };
  }
  makeJavaMethodWrapper(e, t, s) {
    const n = this;
    return function(...r) {
      return n.handleJavaInvocation(e, t, s, this, r);
    };
  }
  handleJavaInvocation(e, t, s, n, r) {
    const [a, o, i] = s;
    this.invokeJavaHandler(e, a, i, n, r, ">");
    const c = t.apply(n, r), l = this.invokeJavaHandler(e, o, i, n, c, "<");
    return void 0 !== l ? l : c;
  }
  invokeNativeHandler(e, t, s, n, r, a) {
    const o = Date.now() - this.started, i = n.threadId, c = this.updateDepth(i, a), l = n.returnAddress.toString(), d = s.capture_backtraces ? Thread.backtrace(n.context).map((e => e.toString())) : null;
    t.call(n, ((...t) => {
      this.emit([ e, o, i, c, l, d, t.join(" ") ]);
    }), r, this.traceState);
  }
  invokeJavaHandler(e, t, s, n, r, a) {
    const o = Date.now() - this.started, i = Process.getCurrentThreadId(), c = this.updateDepth(i, a), l = (...t) => {
      this.emit([ e, o, i, c, null, null, t.join(" ") ]);
    };
    try {
      return t.call(n, l, r, this.traceState);
    } catch (e) {
      if (void 0 !== e.$h) throw e;
      Script.nextTick((() => {
        throw e;
      }));
    }
  }
  updateDepth(e, t) {
    const s = this.stackDepth;
    let n = s.get(e) ?? 0;
    return ">" === t ? s.set(e, n + 1) : "<" === t && (n--, 0 !== n ? s.set(e, n) : s.delete(e)), 
    n;
  }
  parseFunctionHandler(e, t, s, n) {
    try {
      const t = this.parseHandlerScript(s, e);
      return [ t.onEnter ?? w, t.onLeave ?? w, o() ];
    } catch (e) {
      return n({
        id: t,
        name: s,
        message: e.message
      }), [ w, w, o() ];
    }
  }
  parseInstructionHandler(e, t, s, n) {
    try {
      return [ this.parseHandlerScript(s, e), o() ];
    } catch (e) {
      return n({
        id: t,
        name: s,
        message: e.message
      }), [ w, o() ];
    }
  }
  parseHandlerScript(e, t) {
    const s = `/handlers/${e}.js`;
    return Script.evaluate(s, t);
  }
  includeModule(e, t) {
    const {native: s} = t;
    for (const t of this.getModuleResolver().enumerateMatches(`exports:${e}!*`)) s.set(t.address.toString(), c(t));
  }
  excludeModule(e, t) {
    const {native: s} = t;
    for (const t of this.getModuleResolver().enumerateMatches(`exports:${e}!*`)) s.delete(t.address.toString());
  }
  includeFunction(e, t) {
    const s = h(e), {native: n} = t;
    for (const e of this.getModuleResolver().enumerateMatches(`exports:${s.module}!${s.function}`)) n.set(e.address.toString(), c(e));
  }
  excludeFunction(e, t) {
    const s = h(e), {native: n} = t;
    for (const e of this.getModuleResolver().enumerateMatches(`exports:${s.module}!${s.function}`)) n.delete(e.address.toString());
  }
  includeRelativeFunction(e, t) {
    const s = f(e), n = Module.getBaseAddress(s.module).add(s.offset);
    t.native.set(n.toString(), [ "c", s.module, `sub_${s.offset.toString(16)}` ]);
  }
  includeAbsoluteInstruction(e, t) {
    const s = t.modules.find(e);
    null !== s ? t.native.set(e.toString(), [ "insn", s.path, `insn_${e.sub(s.base).toString(16)}` ]) : t.native.set(e.toString(), [ "insn", "", `insn_${e.toString(16)}` ]);
  }
  includeImports(e, t) {
    let s;
    if (null === e) {
      const e = Process.enumerateModules()[0].path;
      s = this.getModuleResolver().enumerateMatches(`imports:${e}!*`);
    } else s = this.getModuleResolver().enumerateMatches(`imports:${e}!*`);
    const {native: n} = t;
    for (const e of s) n.set(e.address.toString(), c(e));
  }
  includeObjCMethod(e, t) {
    const {native: s} = t;
    for (const t of this.getObjcResolver().enumerateMatches(e)) s.set(t.address.toString(), l(t));
  }
  excludeObjCMethod(e, t) {
    const {native: s} = t;
    for (const t of this.getObjcResolver().enumerateMatches(e)) s.delete(t.address.toString());
  }
  includeSwiftFunc(e, t) {
    const {native: s} = t;
    for (const t of this.getSwiftResolver().enumerateMatches(`functions:${e}`)) s.set(t.address.toString(), d(t));
  }
  excludeSwiftFunc(e, t) {
    const {native: s} = t;
    for (const t of this.getSwiftResolver().enumerateMatches(`functions:${e}`)) s.delete(t.address.toString());
  }
  includeJavaMethod(e, t) {
    const s = t.java, n = Java.enumerateMethods(e);
    for (const e of n) {
      const {loader: t} = e, n = g(s, (e => {
        const {loader: s} = e;
        return null !== s && null !== t ? s.equals(t) : s === t;
      }));
      if (void 0 === n) {
        s.push(m(e));
        continue;
      }
      const {classes: r} = n;
      for (const t of e.classes) {
        const {name: e} = t, s = r.get(e);
        if (void 0 === s) {
          r.set(e, p(t));
          continue;
        }
        const {methods: n} = s;
        for (const e of t.methods) {
          const t = v(e), s = n.get(t);
          void 0 === s ? n.set(t, e) : n.set(t, e.length > s.length ? e : s);
        }
      }
    }
  }
  excludeJavaMethod(e, t) {
    const s = t.java, n = Java.enumerateMethods(e);
    for (const e of n) {
      const {loader: t} = e, n = g(s, (e => {
        const {loader: s} = e;
        return null !== s && null !== t ? s.equals(t) : s === t;
      }));
      if (void 0 === n) continue;
      const {classes: r} = n;
      for (const t of e.classes) {
        const {name: e} = t, s = r.get(e);
        if (void 0 === s) continue;
        const {methods: n} = s;
        for (const e of t.methods) {
          const t = v(e);
          n.delete(t);
        }
      }
    }
  }
  includeDebugSymbol(e, t) {
    const {native: s} = t;
    for (const t of DebugSymbol.findFunctionsMatching(e)) s.set(t.toString(), u(t));
  }
  emit(e) {
    this.pendingEvents.push(e), null === this.flushTimer && (this.flushTimer = setTimeout(this.flush, 50));
  }
  getModuleResolver() {
    let e = this.cachedModuleResolver;
    return null === e && (e = new ApiResolver("module"), this.cachedModuleResolver = e), 
    e;
  }
  getObjcResolver() {
    let e = this.cachedObjcResolver;
    if (null === e) {
      try {
        e = new ApiResolver("objc");
      } catch (e) {
        throw new Error("Objective-C runtime is not available");
      }
      this.cachedObjcResolver = e;
    }
    return e;
  }
  getSwiftResolver() {
    let e = this.cachedSwiftResolver;
    if (null === e) {
      try {
        e = new ApiResolver("swift");
      } catch (e) {
        throw new Error("Swift runtime is not available");
      }
      this.cachedSwiftResolver = e;
    }
    return e;
  }
}

async function a(e) {
  const t = [], {type: s, flavor: r, baseId: a} = e, o = e.scopes.slice().map((({name: e, members: t, addresses: s}) => ({
    name: e,
    members: t.slice(),
    addresses: s?.slice()
  })));
  let c = a;
  do {
    const e = [], a = {
      type: s,
      flavor: r,
      baseId: c,
      scopes: e
    };
    let l = 0;
    for (const {name: t, members: s, addresses: r} of o) {
      const a = Math.min(s.length, n - l);
      if (0 === a) break;
      e.push({
        name: t,
        members: s.splice(0, a),
        addresses: r?.splice(0, a)
      }), l += a;
    }
    for (;0 !== o.length && 0 === o[0].members.length; ) o.splice(0, 1);
    send(a);
    const d = await i(`reply:${c}`);
    t.push(...d.scripts), c += l;
  } while (0 !== o.length);
  return {
    scripts: t
  };
}

function o() {
  return {
    capture_backtraces: !1
  };
}

function i(e) {
  return new Promise((t => {
    recv(e, (e => {
      t(e);
    }));
  }));
}

function c(e) {
  const [t, s] = e.name.split("!").slice(-2);
  return [ "c", t, s ];
}

function l(e) {
  const {name: t} = e, [s, n] = t.substr(2, t.length - 3).split(" ", 2);
  return [ "objc", s, [ n, t ] ];
}

function d(e) {
  const {name: t} = e, [s, n] = t.split("!", 2);
  return [ "swift", s, n ];
}

function u(e) {
  const t = DebugSymbol.fromAddress(e);
  return [ "c", t.moduleName ?? "", t.name ];
}

function h(e) {
  const t = e.split("!", 2);
  let s, n;
  return 1 === t.length ? (s = "*", n = t[0]) : (s = "" === t[0] ? "*" : t[0], n = "" === t[1] ? "*" : t[1]), 
  {
    module: s,
    function: n
  };
}

function f(e) {
  const t = e.split("!", 2);
  return {
    module: t[0],
    offset: parseInt(t[1], 16)
  };
}

function m(e) {
  return {
    loader: e.loader,
    classes: new Map(e.classes.map((e => [ e.name, p(e) ])))
  };
}

function p(e) {
  return {
    methods: new Map(e.methods.map((e => [ v(e), e ])))
  };
}

function v(e) {
  const t = e.indexOf("(");
  return -1 === t ? e : e.substr(0, t);
}

function g(e, t) {
  for (const s of e) if (t(s)) return s;
}

function w() {}

class b {
  constructor() {
    this.native = new Map, this.java = [], e.set(this, null);
  }
  get modules() {
    let n = t(this, e, "f");
    return null === n && (n = new ModuleMap, s(this, e, n, "f")), n;
  }
}

e = new WeakMap;

const M = new r;

rpc.exports = {
  init: M.init.bind(M),
  dispose: M.dispose.bind(M),
  updateHandlerCode: M.updateHandlerCode.bind(M),
  updateHandlerConfig: M.updateHandlerConfig.bind(M),
  stageTargets: M.stageTargets.bind(M),
  commitTargets: M.commitTargets.bind(M),
  readMemory: M.readMemory.bind(M),
  resolveAddresses: M.resolveAddresses.bind(M)
};

}).call(this)}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})

},{}]},{},[1])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJhZ2VudC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTs7Ozs7Ozs7Ozs7Ozs7O0FDQUEsTUFBTSxJQUEyQjs7QUFFakMsTUFBTTtFQUFOLFdBQUE7SUFDWSxLQUFBLFdBQVcsSUFBSSxLQUNmLEtBQUEsZ0JBQWdCLElBQUksS0FDcEIsS0FBQSxvQkFBNkM7SUFDN0MsS0FBQSxhQUFhLElBQUksS0FDakIsS0FBQSxhQUF5QixJQUN6QixLQUFBLFNBQVMsR0FDVCxLQUFBLFVBQVUsS0FBSztJQUVmLEtBQUEsZ0JBQThCLElBQzlCLEtBQUEsYUFBa0IsTUFFbEIsS0FBQSx1QkFBMkM7SUFDM0MsS0FBQSxxQkFBeUMsTUFDekMsS0FBQSxzQkFBMEMsTUEwTTFDLEtBQUEsZUFBdUMsRUFBRyxPQUFJLFNBQU07TUFDeEQsS0FBSztRQUNELE1BQU07UUFDTjtRQUNBLFNBQVMsYUFBYSxPQUFVOztBQUNsQyxPQTBqQkUsS0FBQSxRQUFRO01BTVosSUFMd0IsU0FBcEIsS0FBSyxlQUNMLGFBQWEsS0FBSyxhQUNsQixLQUFLLGFBQWE7TUFHWSxNQUE5QixLQUFLLGNBQWMsUUFDbkI7TUFHSixNQUFNLElBQVMsS0FBSztNQUNwQixLQUFLLGdCQUFnQixJQUVyQixLQUFLO1FBQ0QsTUFBTTtRQUNOOztBQUNGO0FBcUNWO0VBNXpCSSxJQUFBLENBQUssR0FBYyxHQUE2QixHQUEyQjtJQUN2RSxNQUFNLElBQUk7SUFDVixFQUFFLFFBQVEsR0FDVixFQUFFLGFBQWEsR0FDZixFQUFFLFFBQVEsS0FBSyxZQUNmLEVBQUUsZ0JBQWdCLEtBQUs7SUFFdkIsS0FBSyxNQUFNLEtBQVUsR0FDakI7T0FDSSxHQUFJLE1BQU0sRUFBTztNQUNuQixPQUFPO01BQ0wsTUFBTSxJQUFJLE1BQU0sa0JBQWtCLEVBQU8sYUFBYSxFQUFFOztJQVdoRSxPQVBBLEtBQUssTUFBTSxHQUFNLE9BQU07TUFDbkIsS0FBSztRQUNELE1BQU07UUFDTixTQUFTLEVBQUU7O0FBQ2IsU0FHQztNQUNILElBQUksUUFBUTtNQUNaLFVBQVUsUUFBUTtNQUNsQixNQUFNLFFBQVE7TUFDZCxjQUFjLFFBQVE7TUFDdEIsV0FBVyxRQUFRO01BQ25CLGFBQWEsUUFBUTs7QUFFN0I7RUFFQSxPQUFBO0lBQ0ksS0FBSztBQUNUO0VBRUEsaUJBQUEsQ0FBa0IsR0FBbUIsR0FBYztJQUMvQyxNQUFNLElBQVUsS0FBSyxTQUFTLElBQUk7SUFDbEMsU0FBZ0IsTUFBWixHQUNBLE1BQU0sSUFBSSxNQUFNO0lBR3BCLElBQXVCLE1BQW5CLEVBQVEsUUFBYztNQUN0QixNQUFNLElBQWEsS0FBSyxxQkFBcUIsR0FBUSxHQUFJLEdBQU0sS0FBSztNQUNwRSxFQUFRLEtBQUssRUFBVyxJQUN4QixFQUFRLEtBQUssRUFBVztXQUNyQjtNQUNILE1BQU0sSUFBYSxLQUFLLHdCQUF3QixHQUFRLEdBQUksR0FBTSxLQUFLO01BQ3ZFLEVBQVEsS0FBSyxFQUFXOztBQUVoQztFQUVBLG1CQUFBLENBQW9CLEdBQW1CO0lBQ25DLE1BQU0sSUFBVSxLQUFLLFNBQVMsSUFBSTtJQUNsQyxTQUFnQixNQUFaLEdBQ0EsTUFBTSxJQUFJLE1BQU07SUFHcEIsRUFBUSxLQUFLO0FBQ2pCO0VBRUEsa0JBQU0sQ0FBYTtJQUNmLE1BQU0sVUFBZ0IsS0FBSyxXQUFXO0lBQ3RDLEtBQUssb0JBQW9CLFNBQ25CLEVBQVE7SUFDZCxPQUFNLE1BQUUsS0FBUyxHQUVYLElBQXNCO0lBQzVCLElBQUksSUFBbUI7SUFDdkIsS0FBSyxPQUFPLEdBQU0sR0FBTyxNQUFXLEVBQUssT0FBTyxVQUM1QyxFQUFNLEtBQUssRUFBRSxHQUFJLEdBQU8sTUFDeEI7SUFFSixLQUFNO0lBQ04sS0FBSyxNQUFNLEtBQVMsRUFBSyxNQUNyQixLQUFLLE9BQU8sR0FBVyxNQUFpQixFQUFNLFFBQVEsV0FDbEQsS0FBSyxNQUFNLEtBQWMsRUFBYSxRQUFRLFVBQzFDLEVBQU0sS0FBSyxFQUFFLEdBQUksR0FBVztJQUM1QjtJQUlaLE9BQU87QUFDWDtFQUVBLG1CQUFNLENBQWM7SUFDaEIsTUFBTSxJQUFVLEtBQUs7SUFDckIsS0FBSyxvQkFBb0I7SUFFekIsS0FBSSxNQUFFLEtBQVM7SUFDSixTQUFQLE1BQ0EsSUFBTyxLQUFLLGVBQWUsR0FBTTtJQUdyQyxNQUFNLElBQTRCLElBQzVCLElBQWtDO01BQ3BDLEVBQVksS0FBSztBQUFFLE9BR2pCLFVBQWtCLEtBQUssbUJBQW1CLEVBQUssUUFBUTtJQUU3RCxJQUFJLElBQTJCO0lBUy9CLE9BUnlCLE1BQXJCLEVBQUssS0FBSyxXQUNWLFVBQWdCLElBQUksU0FBeUIsQ0FBQyxHQUFTO01BQ25ELEtBQUssU0FBUTtRQUNULEtBQUssaUJBQWlCLEVBQUssTUFBTSxHQUFTLEtBQUssR0FBUztBQUFPO0FBQ2pFLFVBSUg7TUFDSCxLQUFLLEtBQUksTUFBYztNQUN2QixRQUFROztBQUVoQjtFQUVBLFVBQUEsQ0FBVyxHQUFpQjtJQUN4QjtNQUNJLE9BQU8sSUFBSSxHQUFTLGNBQWM7TUFDcEMsT0FBTztNQUNMLE9BQU87O0FBRWY7RUFFQSxnQkFBQSxDQUFpQjtJQUNiLElBQUksSUFBa0M7SUFDdEMsT0FBTyxFQUNGLElBQUksS0FDSixJQUFJLFlBQVksYUFDaEIsS0FBSTtNQUNELElBQWlCLFNBQWIsRUFBSSxNQUFlO1FBQ0csU0FBbEIsTUFDQSxJQUFnQixJQUFJO1FBRXhCLE1BQU0sSUFBUyxFQUFjLEtBQUssRUFBSTtRQUN0QyxJQUFlLFNBQVgsR0FDQSxPQUFPLEdBQUcsRUFBTyxRQUFRLEVBQUksUUFBUSxJQUFJLEVBQU87O01BR3hELE9BQU87QUFBRyxRQUViLEtBQUksS0FBSyxFQUFFO0FBQ3BCO0VBRVEsY0FBQSxDQUFlLEdBQWlCO0lBQ3BDLElBQUk7SUFFSixJQUFJLElBQUssR0FBRztNQUNSLEtBQWU7TUFDZixLQUFLLE1BQU0sS0FBUyxFQUFLLE1BQ3JCLEtBQUssT0FBTyxHQUFXLE1BQWlCLEVBQU0sUUFBUSxXQUNsRCxLQUFLLE9BQU8sR0FBWSxNQUEwQixFQUFhLFFBQVEsV0FBVztRQUM5RSxJQUFJLE1BQWdCLEdBQUk7VUFDcEIsTUFDTSxJQUFnQztZQUFFLFNBRGpCLElBQUksSUFBSSxFQUFDLEVBQUMsR0FBWTthQUV2QyxJQUFnQztZQUFFLFFBQVEsRUFBTTtZQUFRLFNBQVMsSUFBSSxJQUFJLEVBQUMsRUFBQyxHQUFXO2FBQ3RGLElBQWMsSUFBSTtVQUV4QixPQURBLEVBQVksS0FBSyxLQUFLLElBQ2Y7O1FBRVg7O1dBSVQ7TUFDSCxJQUFjO01BQ2QsS0FBSyxPQUFPLEdBQUcsTUFBTSxFQUFLLE9BQU8sV0FBVztRQUN4QyxJQUFJLE1BQWdCLEdBQUk7VUFDcEIsTUFBTSxJQUFjLElBQUk7VUFFeEIsT0FEQSxFQUFZLE9BQU8sSUFBSSxHQUFHLElBQ25COztRQUVYOzs7SUFJUixNQUFNLElBQUksTUFBTTtBQUNwQjtFQUVRLFdBQU0sQ0FBTTtJQUNoQixNQUlNLFVBQWdCLEtBQUssV0FBVyxJQUpsQixNQUFPO1lBQ2pCLEtBQUssaUJBQWlCLEVBQUssTUFBTSxLQUFLO0FBQWE7VUFLdkQsS0FBSyxtQkFBbUIsRUFBUSxLQUFLLFFBQVEsS0FBSyxlQUV4RCxLQUFLO01BQ0QsTUFBTTtRQUdWLEVBQVEsTUFBTSxNQUFLO01BQ2YsS0FBSztRQUNELE1BQU07UUFDTixPQUFPLEtBQUssU0FBUzs7QUFDdkI7QUFFVjtFQVVRLGdCQUFNLENBQVcsR0FDakIsSUFBa0Q7SUFDdEQsTUFBTSxJQUFPLElBQUksR0FFWCxJQUF3RDtJQUM5RCxLQUFLLE9BQU8sR0FBVyxHQUFPLE1BQVksR0FDdEMsUUFBUTtLQUNKLEtBQUs7TUFDaUIsY0FBZCxJQUNBLEtBQUssY0FBYyxHQUFTLEtBRTVCLEtBQUssY0FBYyxHQUFTO01BRWhDOztLQUNKLEtBQUs7TUFDaUIsY0FBZCxJQUNBLEtBQUssZ0JBQWdCLEdBQVMsS0FFOUIsS0FBSyxnQkFBZ0IsR0FBUztNQUVsQzs7S0FDSixLQUFLO01BQ2lCLGNBQWQsS0FDQSxLQUFLLHdCQUF3QixHQUFTO01BRTFDOztLQUNKLEtBQUs7TUFDaUIsY0FBZCxLQUNBLEtBQUssMkJBQTJCLElBQUksSUFBVTtNQUVsRDs7S0FDSixLQUFLO01BQ2lCLGNBQWQsS0FDQSxLQUFLLGVBQWUsR0FBUztNQUVqQzs7S0FDSixLQUFLO01BQ2lCLGNBQWQsSUFDQSxLQUFLLGtCQUFrQixHQUFTLEtBRWhDLEtBQUssa0JBQWtCLEdBQVM7TUFFcEM7O0tBQ0osS0FBSztNQUNpQixjQUFkLElBQ0EsS0FBSyxpQkFBaUIsR0FBUyxLQUUvQixLQUFLLGlCQUFpQixHQUFTO01BRW5DOztLQUNKLEtBQUs7TUFDRCxFQUFZLEtBQUssRUFBQyxHQUFXO01BQzdCOztLQUNKLEtBQUs7TUFDaUIsY0FBZCxLQUNBLEtBQUssbUJBQW1CLEdBQVM7O0lBTWpELEtBQUssTUFBTSxLQUFXLEVBQUssT0FBTyxRQUMxQixLQUFLLGNBQWMsSUFBSSxNQUN2QixFQUFLLE9BQU8sT0FBTztJQUkzQixJQUFJLEdBQ0EsS0FBb0I7SUFDeEIsSUFBSSxFQUFZLFNBQVMsR0FBRztNQUN4QixLQUFLLEtBQUssV0FDTixNQUFNLElBQUksTUFBTTtNQUdwQixJQUFtQixJQUFJLFNBQVEsQ0FBQyxHQUFTO1FBQ3JDLEtBQUssU0FBUTtVQUNULEtBQW9CO1VBRXBCO1lBQ0ksS0FBSyxPQUFPLEdBQVcsTUFBWSxHQUNiLGNBQWQsSUFDQSxLQUFLLGtCQUFrQixHQUFTLEtBRWhDLEtBQUssa0JBQWtCLEdBQVM7a0JBSWxDLEVBQVksSUFFbEI7WUFDRixPQUFPO1lBQ0wsRUFBTzs7O0FBRWI7V0FHTixJQUFtQixRQUFRO0lBTy9CLE9BSkssV0FDSyxHQUdIO01BQUU7TUFBTSxPQUFPOztBQUMxQjtFQUVRLHdCQUFNLENBQW1CLEdBQXdCO0lBQ3JELE1BQU0sSUFBYSxJQUFJLEtBQ2pCLElBQVUsSUFBSSxLQUNkLElBQWEsSUFBSSxLQUNqQixJQUFjLElBQUk7SUFFeEIsS0FBSyxPQUFPLElBQUssR0FBTSxHQUFPLE9BQVUsRUFBUSxXQUFXO01BQ3ZELElBQUk7TUFDSixRQUFRO09BQ0osS0FBSztRQUNELElBQVU7UUFDVjs7T0FDSixLQUFLO1FBQ0QsSUFBVTtRQUNWOztPQUNKLEtBQUs7UUFDRCxJQUFVO1FBQ1Y7O09BQ0osS0FBSztRQUNELElBQVU7O01BSWxCLElBQUksSUFBUSxFQUFRLElBQUk7V0FDVixNQUFWLE1BQ0EsSUFBUSxJQUNSLEVBQVEsSUFBSSxHQUFPLEtBR3ZCLEVBQU0sS0FBSyxFQUFDLEdBQU0sSUFBSTs7SUFHMUIsT0FBTyxHQUFNLEdBQVMsV0FBa0IsUUFBUSxJQUFJLEVBQ2hELEtBQUssbUJBQW1CLFFBQVEsR0FBWSxJQUM1QyxLQUFLLG1CQUFtQixLQUFLLEdBQVMsSUFDdEMsS0FBSyxtQkFBbUIsUUFBUSxHQUFZLElBQzVDLEtBQUssbUJBQW1CLFNBQVMsR0FBYTtJQUdsRCxPQUFPLEtBQUksTUFBUyxNQUFZO0FBQ3BDO0VBRVEsd0JBQU0sQ0FBbUIsR0FBNEIsR0FBNEI7SUFFckYsSUFBb0IsTUFBaEIsRUFBTyxNQUNQLE9BQU87SUFHWCxNQUFNLElBQVMsS0FBSyxRQUNkLElBQWdDLElBQ2hDLElBQTBCO01BQzVCLE1BQU07TUFDTjtNQUNBO01BQ0E7O0lBRUosS0FBSyxPQUFPLEdBQU0sTUFBVSxFQUFPLFdBQy9CLEVBQU8sS0FBSztNQUNSO01BQ0EsU0FBUyxFQUFNLEtBQUksS0FBUSxFQUFLO01BQ2hDLFdBQVcsRUFBTSxLQUFJLEtBQVEsRUFBSyxHQUFHO1FBRXpDLEtBQUssVUFBVSxFQUFNO0lBR3pCLE9BQU0sU0FBRSxXQUFtQyxFQUFZLElBRWpELElBQXVCO0lBQzdCLElBQUksSUFBUztJQUNiLE1BQU0sSUFBMkIsV0FBWDtJQUN0QixLQUFLLE1BQU0sS0FBUyxFQUFPLFVBQ3ZCLEtBQUssT0FBTyxHQUFNLE1BQVksR0FBTztNQUNqQyxNQUFNLElBQUssSUFBUyxHQUNkLElBQStCLG1CQUFULElBQXFCLElBQU8sRUFBSyxJQUV2RCxJQUFVLElBQ1YsS0FBSyx3QkFBd0IsRUFBUSxJQUFTLEdBQUksR0FBYSxLQUMvRCxLQUFLLHFCQUFxQixFQUFRLElBQVMsR0FBSSxHQUFhO01BQ2xFLEtBQUssU0FBUyxJQUFJLEdBQUksSUFDdEIsS0FBSyxjQUFjLElBQUksRUFBUTtNQUUvQjtRQUNJLFlBQVksT0FBTyxHQUFTLElBQ2xCLEtBQUssOEJBQThCLEdBQUksS0FDdkMsS0FBSywyQkFBMkIsR0FBSTtRQUNoRCxPQUFPO1FBQ0wsRUFBUTtVQUFFO1VBQUksTUFBTTtVQUFhLFNBQVUsRUFBWTs7O01BRzNELEVBQUksS0FBSyxJQUNUOztJQUdSLE9BQU87QUFDWDtFQUVRLHNCQUFNLENBQWlCLEdBQTJCO0lBQ3RELE1BQU0sSUFBUyxLQUFLLFFBQ2QsSUFBZ0MsSUFDaEMsSUFBMEI7TUFDNUIsTUFBTTtNQUNOLFFBQVE7TUFDUjtNQUNBOztJQUVKLEtBQUssTUFBTSxLQUFTLEdBQ2hCLEtBQUssT0FBTyxJQUFXLFNBQUUsT0FBYyxFQUFNLFFBQVEsV0FBVztNQUM1RCxNQUFNLElBQWlCLEVBQVUsTUFBTSxNQUNqQyxJQUFnQixFQUFlLEVBQWUsU0FBUyxJQUN2RCxJQUF3QixNQUFNLEtBQUssRUFBUSxRQUFRLEtBQUksS0FBWSxFQUFDLEdBQVUsR0FBRyxLQUFpQjtNQUN4RyxFQUFPLEtBQUs7UUFDUixNQUFNO1FBQ047VUFFSixLQUFLLFVBQVUsRUFBUTs7SUFJL0IsT0FBTSxTQUFFLFdBQW1DLEVBQVk7SUFFdkQsT0FBTyxJQUFJLFNBQXlCO01BQ2hDLEtBQUssU0FBUTtRQUNULE1BQU0sSUFBdUI7UUFDN0IsSUFBSSxJQUFTO1FBQ2IsS0FBSyxNQUFNLEtBQVMsR0FBUTtVQUN4QixNQUFNLElBQVUsS0FBSyxhQUFhLElBQUksRUFBTTtVQUU1QyxLQUFLLE9BQU8sSUFBVyxTQUFFLE9BQWMsRUFBTSxRQUFRLFdBQVc7WUFDNUQsTUFBTSxJQUFJLEVBQVEsSUFBSTtZQUV0QixLQUFLLE9BQU8sR0FBVSxNQUFhLEVBQVEsV0FBVztjQUNsRCxNQUFNLElBQUssSUFBUyxHQUVkLElBQVUsS0FBSyxxQkFBcUIsRUFBUSxJQUFTLEdBQUksR0FBVTtjQUN6RSxLQUFLLFNBQVMsSUFBSSxHQUFJO2NBRXRCLE1BQU0sSUFBb0MsRUFBRTtjQUM1QyxLQUFLLE1BQU0sS0FBVSxFQUFXLFdBQzVCLEVBQU8saUJBQWlCLEtBQUssc0JBQXNCLEdBQUksR0FBUTtjQUduRSxFQUFJLEtBQUssSUFDVDs7OztRQUtaLEVBQVE7QUFBSTtBQUNkO0FBRVY7RUFFUSwwQkFBQSxDQUEyQixHQUFtQjtJQUNsRCxNQUFNLElBQVE7SUFFZCxPQUFPO01BQ0gsT0FBQSxDQUFRO1FBQ0osT0FBTyxHQUFTLEdBQUcsS0FBVTtRQUM3QixFQUFNLG9CQUFvQixHQUFJLEdBQVMsR0FBUSxNQUFNLEdBQU07QUFDL0Q7TUFDQSxPQUFBLENBQVE7UUFDSixPQUFPLEdBQUcsR0FBUyxLQUFVO1FBQzdCLEVBQU0sb0JBQW9CLEdBQUksR0FBUyxHQUFRLE1BQU0sR0FBUTtBQUNqRTs7QUFFUjtFQUVRLDZCQUFBLENBQThCLEdBQW1CO0lBQ3JELE1BQU0sSUFBUTtJQUVkLE9BQU8sU0FBVTtNQUNiLE9BQU8sR0FBTyxLQUFVO01BQ3hCLEVBQU0sb0JBQW9CLEdBQUksR0FBTyxHQUFRLE1BQU0sR0FBTTtBQUM3RDtBQUNKO0VBRVEscUJBQUEsQ0FBc0IsR0FBbUIsR0FBcUI7SUFDbEUsTUFBTSxJQUFRO0lBRWQsT0FBTyxZQUFhO01BQ2hCLE9BQU8sRUFBTSxxQkFBcUIsR0FBSSxHQUFRLEdBQVMsTUFBTTtBQUNqRTtBQUNKO0VBRVEsb0JBQUEsQ0FBcUIsR0FBbUIsR0FBcUIsR0FBK0IsR0FBd0I7SUFDeEgsT0FBTyxHQUFTLEdBQVMsS0FBVTtJQUVuQyxLQUFLLGtCQUFrQixHQUFJLEdBQVMsR0FBUSxHQUFVLEdBQU07SUFFNUQsTUFBTSxJQUFTLEVBQU8sTUFBTSxHQUFVLElBRWhDLElBQW9CLEtBQUssa0JBQWtCLEdBQUksR0FBUyxHQUFRLEdBQVUsR0FBUTtJQUV4RixZQUE4QixNQUF0QixJQUFtQyxJQUFvQjtBQUNuRTtFQUVRLG1CQUFBLENBQW9CLEdBQW1CLEdBQ3ZDLEdBQXVCLEdBQTRCLEdBQVk7SUFDbkUsTUFBTSxJQUFZLEtBQUssUUFBUSxLQUFLLFNBQzlCLElBQVcsRUFBUSxVQUNuQixJQUFRLEtBQUssWUFBWSxHQUFVLElBQ25DLElBQVMsRUFBUSxjQUFjLFlBQy9CLElBQVksRUFBTyxxQkFBcUIsT0FBTyxVQUFVLEVBQVEsU0FBUyxLQUFJLEtBQUssRUFBRSxlQUFjO0lBTXpHLEVBQVMsS0FBSyxJQUpGLElBQUk7TUFDWixLQUFLLEtBQUssRUFBQyxHQUFJLEdBQVcsR0FBVSxHQUFPLEdBQVEsR0FBVyxFQUFRLEtBQUs7QUFBTSxRQUd6RCxHQUFPLEtBQUs7QUFDNUM7RUFFUSxpQkFBQSxDQUFrQixHQUFtQixHQUFpRCxHQUN0RixHQUF3QixHQUFZO0lBQ3hDLE1BQU0sSUFBWSxLQUFLLFFBQVEsS0FBSyxTQUM5QixJQUFXLFFBQVEsc0JBQ25CLElBQVEsS0FBSyxZQUFZLEdBQVUsSUFFbkMsSUFBTSxJQUFJO01BQ1osS0FBSyxLQUFLLEVBQUMsR0FBSSxHQUFXLEdBQVUsR0FBTyxNQUFNLE1BQU0sRUFBUSxLQUFLO0FBQU07SUFHOUU7TUFDSSxPQUFPLEVBQVMsS0FBSyxHQUFVLEdBQUssR0FBTyxLQUFLO01BQ2xELE9BQU87TUFFTCxTQURpQyxNQUFULEVBQUUsSUFFdEIsTUFBTTtNQUVOLE9BQU8sVUFBUztRQUFRLE1BQU07QUFBQzs7QUFHM0M7RUFFUSxXQUFBLENBQVksR0FBb0I7SUFDcEMsTUFBTSxJQUFlLEtBQUs7SUFFMUIsSUFBSSxJQUFRLEVBQWEsSUFBSSxNQUFhO0lBWTFDLE9BWGlCLFFBQWIsSUFDQSxFQUFhLElBQUksR0FBVSxJQUFRLEtBQ2YsUUFBYixNQUNQLEtBQ2MsTUFBVixJQUNBLEVBQWEsSUFBSSxHQUFVLEtBRTNCLEVBQWEsT0FBTztJQUlyQjtBQUNYO0VBRVEsb0JBQUEsQ0FBcUIsR0FBZ0IsR0FBbUIsR0FBYztJQUMxRTtNQUNJLE1BQU0sSUFBSSxLQUFLLG1CQUFtQixHQUFNO01BQ3hDLE9BQU8sRUFBQyxFQUFFLFdBQVcsR0FBTSxFQUFFLFdBQVcsR0FBTTtNQUNoRCxPQUFPO01BRUwsT0FEQSxFQUFRO1FBQUU7UUFBSTtRQUFNLFNBQVUsRUFBWTtVQUNuQyxFQUFDLEdBQU0sR0FBTTs7QUFFNUI7RUFFUSx1QkFBQSxDQUF3QixHQUFnQixHQUFtQixHQUFjO0lBRTdFO01BRUksT0FBTyxFQURPLEtBQUssbUJBQW1CLEdBQU0sSUFDN0I7TUFDakIsT0FBTztNQUVMLE9BREEsRUFBUTtRQUFFO1FBQUk7UUFBTSxTQUFVLEVBQVk7VUFDbkMsRUFBQyxHQUFNOztBQUV0QjtFQUVRLGtCQUFBLENBQW1CLEdBQWM7SUFDckMsTUFBTSxJQUFLLGFBQWE7SUFDeEIsT0FBTyxPQUFPLFNBQVMsR0FBSTtBQUMvQjtFQUVRLGFBQUEsQ0FBYyxHQUFpQjtJQUNuQyxPQUFNLFFBQUUsS0FBVztJQUNuQixLQUFLLE1BQU0sS0FBSyxLQUFLLG9CQUFvQixpQkFBaUIsV0FBVyxRQUNqRSxFQUFPLElBQUksRUFBRSxRQUFRLFlBQVksRUFBOEI7QUFFdkU7RUFFUSxhQUFBLENBQWMsR0FBaUI7SUFDbkMsT0FBTSxRQUFFLEtBQVc7SUFDbkIsS0FBSyxNQUFNLEtBQUssS0FBSyxvQkFBb0IsaUJBQWlCLFdBQVcsUUFDakUsRUFBTyxPQUFPLEVBQUUsUUFBUTtBQUVoQztFQUVRLGVBQUEsQ0FBZ0IsR0FBaUI7SUFDckMsTUFBTSxJQUFJLEVBQTJCLEtBQy9CLFFBQUUsS0FBVztJQUNuQixLQUFLLE1BQU0sS0FBSyxLQUFLLG9CQUFvQixpQkFBaUIsV0FBVyxFQUFFLFVBQVUsRUFBRSxhQUMvRSxFQUFPLElBQUksRUFBRSxRQUFRLFlBQVksRUFBOEI7QUFFdkU7RUFFUSxlQUFBLENBQWdCLEdBQWlCO0lBQ3JDLE1BQU0sSUFBSSxFQUEyQixLQUMvQixRQUFFLEtBQVc7SUFDbkIsS0FBSyxNQUFNLEtBQUssS0FBSyxvQkFBb0IsaUJBQWlCLFdBQVcsRUFBRSxVQUFVLEVBQUUsYUFDL0UsRUFBTyxPQUFPLEVBQUUsUUFBUTtBQUVoQztFQUVRLHVCQUFBLENBQXdCLEdBQWlCO0lBQzdDLE1BQU0sSUFBSSxFQUE2QixJQUNqQyxJQUFVLE9BQU8sZUFBZSxFQUFFLFFBQVEsSUFBSSxFQUFFO0lBQ3RELEVBQUssT0FBTyxJQUFJLEVBQVEsWUFBWSxFQUFDLEtBQUssRUFBRSxRQUFRLE9BQU8sRUFBRSxPQUFPLFNBQVM7QUFDakY7RUFFUSwwQkFBQSxDQUEyQixHQUF3QjtJQUN2RCxNQUFNLElBQVMsRUFBSyxRQUFRLEtBQUs7SUFDbEIsU0FBWCxJQUNBLEVBQUssT0FBTyxJQUFJLEVBQVEsWUFBWSxFQUFDLFFBQVEsRUFBTyxNQUFNLFFBQVEsRUFBUSxJQUFJLEVBQU8sTUFBTSxTQUFTLFdBRXBHLEVBQUssT0FBTyxJQUFJLEVBQVEsWUFBWSxFQUFDLFFBQVEsSUFBSSxRQUFRLEVBQVEsU0FBUztBQUVsRjtFQUVRLGNBQUEsQ0FBZSxHQUFpQjtJQUNwQyxJQUFJO0lBQ0osSUFBZ0IsU0FBWixHQUFrQjtNQUNsQixNQUFNLElBQWEsUUFBUSxtQkFBbUIsR0FBRztNQUNqRCxJQUFVLEtBQUssb0JBQW9CLGlCQUFpQixXQUFXO1dBRS9ELElBQVUsS0FBSyxvQkFBb0IsaUJBQWlCLFdBQVc7SUFHbkUsT0FBTSxRQUFFLEtBQVc7SUFDbkIsS0FBSyxNQUFNLEtBQUssR0FDWixFQUFPLElBQUksRUFBRSxRQUFRLFlBQVksRUFBOEI7QUFFdkU7RUFFUSxpQkFBQSxDQUFrQixHQUFpQjtJQUN2QyxPQUFNLFFBQUUsS0FBVztJQUNuQixLQUFLLE1BQU0sS0FBSyxLQUFLLGtCQUFrQixpQkFBaUIsSUFDcEQsRUFBTyxJQUFJLEVBQUUsUUFBUSxZQUFZLEVBQTBCO0FBRW5FO0VBRVEsaUJBQUEsQ0FBa0IsR0FBaUI7SUFDdkMsT0FBTSxRQUFFLEtBQVc7SUFDbkIsS0FBSyxNQUFNLEtBQUssS0FBSyxrQkFBa0IsaUJBQWlCLElBQ3BELEVBQU8sT0FBTyxFQUFFLFFBQVE7QUFFaEM7RUFFUSxnQkFBQSxDQUFpQixHQUFpQjtJQUN0QyxPQUFNLFFBQUUsS0FBVztJQUNuQixLQUFLLE1BQU0sS0FBSyxLQUFLLG1CQUFtQixpQkFBaUIsYUFBYSxNQUNsRSxFQUFPLElBQUksRUFBRSxRQUFRLFlBQVksRUFBeUI7QUFFbEU7RUFFUSxnQkFBQSxDQUFpQixHQUFpQjtJQUN0QyxPQUFNLFFBQUUsS0FBVztJQUNuQixLQUFLLE1BQU0sS0FBSyxLQUFLLG1CQUFtQixpQkFBaUIsYUFBYSxNQUNsRSxFQUFPLE9BQU8sRUFBRSxRQUFRO0FBRWhDO0VBRVEsaUJBQUEsQ0FBa0IsR0FBaUI7SUFDdkMsTUFBTSxJQUFpQixFQUFLLE1BRXRCLElBQVMsS0FBSyxpQkFBaUI7SUFDckMsS0FBSyxNQUFNLEtBQVMsR0FBUTtNQUN4QixPQUFNLFFBQUUsS0FBVyxHQUViLElBQWdCLEVBQUssSUFBZ0I7UUFDdkMsT0FBUSxRQUFRLEtBQW9CO1FBQ3BDLE9BQXdCLFNBQXBCLEtBQXVDLFNBQVgsSUFDckIsRUFBZ0IsT0FBTyxLQUV2QixNQUFvQjs7TUFHbkMsU0FBc0IsTUFBbEIsR0FBNkI7UUFDN0IsRUFBZSxLQUFLLEVBQThCO1FBQ2xEOztNQUdKLE9BQVEsU0FBUyxLQUFvQjtNQUNyQyxLQUFLLE1BQU0sS0FBUyxFQUFNLFNBQVM7UUFDL0IsT0FBUSxNQUFNLEtBQWMsR0FFdEIsSUFBZ0IsRUFBZ0IsSUFBSTtRQUMxQyxTQUFzQixNQUFsQixHQUE2QjtVQUM3QixFQUFnQixJQUFJLEdBQVcsRUFBOEI7VUFDN0Q7O1FBR0osT0FBUSxTQUFTLEtBQW9CO1FBQ3JDLEtBQUssTUFBTSxLQUFjLEVBQU0sU0FBUztVQUNwQyxNQUFNLElBQWlCLEVBQWlDLElBQ2xELElBQWUsRUFBZ0IsSUFBSTtlQUNwQixNQUFqQixJQUNBLEVBQWdCLElBQUksR0FBZ0IsS0FFcEMsRUFBZ0IsSUFBSSxHQUFpQixFQUFXLFNBQVMsRUFBYSxTQUFVLElBQWE7Ozs7QUFLakg7RUFFUSxpQkFBQSxDQUFrQixHQUFpQjtJQUN2QyxNQUFNLElBQWlCLEVBQUssTUFFdEIsSUFBUyxLQUFLLGlCQUFpQjtJQUNyQyxLQUFLLE1BQU0sS0FBUyxHQUFRO01BQ3hCLE9BQU0sUUFBRSxLQUFXLEdBRWIsSUFBZ0IsRUFBSyxJQUFnQjtRQUN2QyxPQUFRLFFBQVEsS0FBb0I7UUFDcEMsT0FBd0IsU0FBcEIsS0FBdUMsU0FBWCxJQUNyQixFQUFnQixPQUFPLEtBRXZCLE1BQW9COztNQUduQyxTQUFzQixNQUFsQixHQUNBO01BR0osT0FBUSxTQUFTLEtBQW9CO01BQ3JDLEtBQUssTUFBTSxLQUFTLEVBQU0sU0FBUztRQUMvQixPQUFRLE1BQU0sS0FBYyxHQUV0QixJQUFnQixFQUFnQixJQUFJO1FBQzFDLFNBQXNCLE1BQWxCLEdBQ0E7UUFHSixPQUFRLFNBQVMsS0FBb0I7UUFDckMsS0FBSyxNQUFNLEtBQWMsRUFBTSxTQUFTO1VBQ3BDLE1BQU0sSUFBaUIsRUFBaUM7VUFDeEQsRUFBZ0IsT0FBTzs7OztBQUl2QztFQUVRLGtCQUFBLENBQW1CLEdBQWlCO0lBQ3hDLE9BQU0sUUFBRSxLQUFXO0lBQ25CLEtBQUssTUFBTSxLQUFXLFlBQVksc0JBQXNCLElBQ3BELEVBQU8sSUFBSSxFQUFRLFlBQVksRUFBNkI7QUFFcEU7RUFFUSxJQUFBLENBQUs7SUFDVCxLQUFLLGNBQWMsS0FBSyxJQUVBLFNBQXBCLEtBQUssZUFDTCxLQUFLLGFBQWEsV0FBVyxLQUFLLE9BQU87QUFFakQ7RUFxQlEsaUJBQUE7SUFDSixJQUFJLElBQVcsS0FBSztJQUtwQixPQUppQixTQUFiLE1BQ0EsSUFBVyxJQUFJLFlBQVksV0FDM0IsS0FBSyx1QkFBdUI7SUFFekI7QUFDWDtFQUVRLGVBQUE7SUFDSixJQUFJLElBQVcsS0FBSztJQUNwQixJQUFpQixTQUFiLEdBQW1CO01BQ25CO1FBQ0ksSUFBVyxJQUFJLFlBQVk7UUFDN0IsT0FBTztRQUNMLE1BQU0sSUFBSSxNQUFNOztNQUVwQixLQUFLLHFCQUFxQjs7SUFFOUIsT0FBTztBQUNYO0VBRVEsZ0JBQUE7SUFDSixJQUFJLElBQVcsS0FBSztJQUNwQixJQUFpQixTQUFiLEdBQW1CO01BQ25CO1FBQ0ksSUFBVyxJQUFJLFlBQVk7UUFDN0IsT0FBTztRQUNMLE1BQU0sSUFBSSxNQUFNOztNQUVwQixLQUFLLHNCQUFzQjs7SUFFL0IsT0FBTztBQUNYOzs7QUFHSixlQUFlLEVBQVk7RUFDdkIsTUFBTSxJQUEyQixLQUUzQixNQUFFLEdBQUksUUFBRSxHQUFNLFFBQUUsS0FBVyxHQUUzQixJQUFnQixFQUFRLE9BQU8sUUFBUSxLQUFJLEVBQUcsU0FBTSxZQUFTLG1CQUN4RDtJQUNIO0lBQ0EsU0FBUyxFQUFRO0lBQ2pCLFdBQVcsR0FBVzs7RUFHOUIsSUFBSSxJQUFLO0VBQ1QsR0FBRztJQUNDLE1BQU0sSUFBbUMsSUFDbkMsSUFBNkI7TUFDL0I7TUFDQTtNQUNBLFFBQVE7TUFDUixRQUFROztJQUdaLElBQUksSUFBTztJQUNYLEtBQUssT0FBTSxNQUFFLEdBQU0sU0FBUyxHQUFnQixXQUFXLE1BQXNCLEdBQWU7TUFDeEYsTUFBTSxJQUFJLEtBQUssSUFBSSxFQUFlLFFBQVEsSUFBMkI7TUFDckUsSUFBVSxNQUFOLEdBQ0E7TUFFSixFQUFVLEtBQUs7UUFDWDtRQUNBLFNBQVMsRUFBZSxPQUFPLEdBQUc7UUFDbEMsV0FBVyxHQUFrQixPQUFPLEdBQUc7VUFFM0MsS0FBUTs7SUFHWixNQUFnQyxNQUF6QixFQUFjLFVBQW9ELE1BQXBDLEVBQWMsR0FBRyxRQUFRLFVBQzFELEVBQWMsT0FBTyxHQUFHO0lBRzVCLEtBQUs7SUFDTCxNQUFNLFVBQWtDLEVBQWdCLFNBQVM7SUFFakUsRUFBUSxRQUFRLEVBQVMsVUFFekIsS0FBTTtXQUN3QixNQUF6QixFQUFjO0VBRXZCLE9BQU87SUFDSDs7QUFFUjs7QUFFQSxTQUFTO0VBQ0wsT0FBTztJQUNILHFCQUFvQjs7QUFFNUI7O0FBRUEsU0FBUyxFQUFtQjtFQUN4QixPQUFPLElBQUksU0FBUTtJQUNmLEtBQUssSUFBTztNQUNSLEVBQVE7QUFBUztBQUNuQjtBQUVWOztBQUVBLFNBQVMsRUFBOEI7RUFDbkMsT0FBTyxHQUFZLEtBQWdCLEVBQUUsS0FBSyxNQUFNLEtBQUssT0FBTztFQUM1RCxPQUFPLEVBQUMsS0FBSyxHQUFZO0FBQzdCOztBQUVBLFNBQVMsRUFBMEI7RUFDL0IsT0FBTSxNQUFFLEtBQVMsSUFDVixHQUFXLEtBQWMsRUFBSyxPQUFPLEdBQUcsRUFBSyxTQUFTLEdBQUcsTUFBTSxLQUFLO0VBQzNFLE9BQU8sRUFBQyxRQUFRLEdBQVcsRUFBQyxHQUFZO0FBQzVDOztBQUVBLFNBQVMsRUFBeUI7RUFDOUIsT0FBTSxNQUFFLEtBQVMsSUFDVixHQUFZLEtBQWMsRUFBSyxNQUFNLEtBQUs7RUFDakQsT0FBTyxFQUFDLFNBQVMsR0FBWTtBQUNqQzs7QUFFQSxTQUFTLEVBQTZCO0VBQ2xDLE1BQU0sSUFBUyxZQUFZLFlBQVk7RUFDdkMsT0FBTyxFQUFDLEtBQUssRUFBTyxjQUFjLElBQUksRUFBTztBQUNqRDs7QUFFQSxTQUFTLEVBQTJCO0VBQ2hDLE1BQU0sSUFBUyxFQUFRLE1BQU0sS0FBSztFQUVsQyxJQUFJLEdBQUc7RUFTUCxPQVJzQixNQUFsQixFQUFPLFVBQ1AsSUFBSSxLQUNKLElBQUksRUFBTyxPQUVYLElBQW1CLE9BQWQsRUFBTyxLQUFhLE1BQU0sRUFBTyxJQUN0QyxJQUFtQixPQUFkLEVBQU8sS0FBYSxNQUFNLEVBQU87RUFHbkM7SUFDSCxRQUFRO0lBQ1IsVUFBVTs7QUFFbEI7O0FBRUEsU0FBUyxFQUE2QjtFQUNsQyxNQUFNLElBQVMsRUFBUSxNQUFNLEtBQUs7RUFFbEMsT0FBTztJQUNILFFBQVEsRUFBTztJQUNmLFFBQVEsU0FBUyxFQUFPLElBQUk7O0FBRXBDOztBQUVBLFNBQVMsRUFBOEI7RUFDbkMsT0FBTztJQUNILFFBQVEsRUFBTTtJQUNkLFNBQVMsSUFBSSxJQUNULEVBQU0sUUFBUSxLQUFJLEtBQVMsRUFBQyxFQUFNLE1BQU0sRUFBOEI7O0FBRWxGOztBQUVBLFNBQVMsRUFBOEI7RUFDbkMsT0FBTztJQUNILFNBQVMsSUFBSSxJQUNULEVBQU0sUUFBUSxLQUFJLEtBQVksRUFBQyxFQUFpQyxJQUFXOztBQUV2Rjs7QUFFQSxTQUFTLEVBQWlDO0VBQ3RDLE1BQU0sSUFBaUIsRUFBUyxRQUFRO0VBQ3hDLFFBQTRCLE1BQXBCLElBQXlCLElBQVcsRUFBUyxPQUFPLEdBQUc7QUFDbkU7O0FBRUEsU0FBUyxFQUFRLEdBQVk7RUFDekIsS0FBSyxNQUFNLEtBQVcsR0FDbEIsSUFBSSxFQUFVLElBQ1YsT0FBTztBQUduQjs7QUFFQSxTQUFTLEtBQ1Q7O0FBd0RBLE1BQU07RUFBTixXQUFBO0lBQ0ksS0FBQSxTQUF3QixJQUFJLEtBQzVCLEtBQUEsT0FBMEIsSUFFMUIsRUFBQSxJQUFBLE1BQW1DO0FBVXZDO0VBUkksV0FBSTtJQUNBLElBQUksSUFBVSxFQUFBLE1BQUksR0FBQTtJQUtsQixPQUpnQixTQUFaLE1BQ0EsSUFBVSxJQUFJLFdBQ2QsRUFBQSxNQUFJLEdBQWtCLEdBQU8sT0FFMUI7QUFDWDs7Ozs7QUE4RUosTUFBTSxJQUFRLElBQUk7O0FBRWxCLElBQUksVUFBVTtFQUNWLE1BQU0sRUFBTSxLQUFLLEtBQUs7RUFDdEIsU0FBUyxFQUFNLFFBQVEsS0FBSztFQUM1QixtQkFBbUIsRUFBTSxrQkFBa0IsS0FBSztFQUNoRCxxQkFBcUIsRUFBTSxvQkFBb0IsS0FBSztFQUNwRCxjQUFjLEVBQU0sYUFBYSxLQUFLO0VBQ3RDLGVBQWUsRUFBTSxjQUFjLEtBQUs7RUFDeEMsWUFBWSxFQUFNLFdBQVcsS0FBSztFQUNsQyxrQkFBa0IsRUFBTSxpQkFBaUIsS0FBSyIsImZpbGUiOiJnZW5lcmF0ZWQuanMiLCJzb3VyY2VSb290IjoiIn0=
