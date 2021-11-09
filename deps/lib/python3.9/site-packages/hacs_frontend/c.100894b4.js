import{A as t,$ as e,e as i,J as o,a0 as s,j as a,a1 as n,T as r,b as d,r as c,n as l,_ as h,F as p,G as m,a2 as u,m as f,P as g,h as b,au as x,S as v,av as y,R as _,a4 as w,U as I,a9 as E,aa as k,q as T,o as R,M as A,B as C,aw as S,ax as O,ay as F,y as $,z,az as L,a8 as M,C as B,aA as N,a as D,aB as P,aC as H,aD as U,s as j,d as G}from"./main-60575625.js";import{h as V,f as K}from"./c.149491ec.js";import{i as q,s as X}from"./c.daedfab1.js";import{a as W,o as Q}from"./c.5325c693.js";import{P as Y}from"./c.5bd359ff.js";import"./c.75898fa6.js";import{a as J}from"./c.6d478880.js";import"./c.6dff8de3.js";import"./c.659eb0c9.js";import{o as Z}from"./c.e32d17dc.js";import"./c.386ba692.js";import"./c.40bbc652.js";import"./c.3af0c990.js";class tt extends a{constructor(){super(...arguments),this.mini=!1,this.exited=!1,this.disabled=!1,this.extended=!1,this.showIconAtEnd=!1,this.reducedTouchTarget=!1,this.icon="",this.label="",this.shouldRenderRipple=!1,this.useStateLayerCustomProperties=!1,this.rippleHandlers=new n(()=>(this.shouldRenderRipple=!0,this.ripple))}render(){const t=this.mini&&!this.reducedTouchTarget,e={"mdc-fab--mini":this.mini,"mdc-fab--touch":t,"mdc-fab--exited":this.exited,"mdc-fab--extended":this.extended,"icon-end":this.showIconAtEnd},i=this.label?this.label:this.icon;return r`<button
          class="mdc-fab ${d(e)}"
          ?disabled="${this.disabled}"
          aria-label="${i}"
          @mouseenter=${this.handleRippleMouseEnter}
          @mouseleave=${this.handleRippleMouseLeave}
          @focus=${this.handleRippleFocus}
          @blur=${this.handleRippleBlur}
          @mousedown=${this.handleRippleActivate}
          @touchstart=${this.handleRippleStartPress}
          @touchend=${this.handleRippleDeactivate}
          @touchcancel=${this.handleRippleDeactivate}><!--
        -->${this.renderBeforeRipple()}<!--
        -->${this.renderRipple()}<!--
        -->${this.showIconAtEnd?this.renderLabel():""}<!--
        --><span class="material-icons mdc-fab__icon"><!--
          --><slot name="icon">${this.icon}</slot><!--
       --></span><!--
        -->${this.showIconAtEnd?"":this.renderLabel()}<!--
        -->${this.renderTouchTarget()}<!--
      --></button>`}renderIcon(){return r``}renderTouchTarget(){const t=this.mini&&!this.reducedTouchTarget;return r`${t?r`<div class="mdc-fab__touch"></div>`:""}`}renderLabel(){const t=""!==this.label&&this.extended;return r`${t?r`<span class="mdc-fab__label">${this.label}</span>`:""}`}renderBeforeRipple(){return r``}renderRipple(){return this.shouldRenderRipple?r`<mwc-ripple class="ripple"
        .internalUseStateLayerCustomProperties="${this.useStateLayerCustomProperties}"
         ></mwc-ripple>`:""}handleRippleActivate(t){const e=()=>{window.removeEventListener("mouseup",e),this.handleRippleDeactivate()};window.addEventListener("mouseup",e),this.handleRippleStartPress(t)}handleRippleStartPress(t){this.rippleHandlers.startPress(t)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}tt.shadowRootOptions={mode:"open",delegatesFocus:!0},t([e("mwc-ripple")],tt.prototype,"ripple",void 0),t([i({type:Boolean})],tt.prototype,"mini",void 0),t([i({type:Boolean})],tt.prototype,"exited",void 0),t([i({type:Boolean})],tt.prototype,"disabled",void 0),t([i({type:Boolean})],tt.prototype,"extended",void 0),t([i({type:Boolean})],tt.prototype,"showIconAtEnd",void 0),t([i({type:Boolean})],tt.prototype,"reducedTouchTarget",void 0),t([i()],tt.prototype,"icon",void 0),t([i()],tt.prototype,"label",void 0),t([o()],tt.prototype,"shouldRenderRipple",void 0),t([o()],tt.prototype,"useStateLayerCustomProperties",void 0),t([s({passive:!0})],tt.prototype,"handleRippleStartPress",null);const et=c`:host .mdc-fab .material-icons{font-family:var(--mdc-icon-font, "Material Icons");font-weight:normal;font-style:normal;font-size:var(--mdc-icon-size, 24px);line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;-moz-osx-font-smoothing:grayscale;font-feature-settings:"liga"}:host{outline:none;--mdc-ripple-color: currentcolor;user-select:none;-webkit-tap-highlight-color:transparent;display:inline-flex;-webkit-tap-highlight-color:transparent;display:inline-flex;outline:none;user-select:none}:host .mdc-touch-target-wrapper{display:inline}:host .mdc-elevation-overlay{position:absolute;border-radius:inherit;pointer-events:none;opacity:0;opacity:var(--mdc-elevation-overlay-opacity, 0);transition:opacity 280ms cubic-bezier(0.4, 0, 0.2, 1);background-color:#fff;background-color:var(--mdc-elevation-overlay-color, #fff)}:host .mdc-fab{position:relative;display:inline-flex;position:relative;align-items:center;justify-content:center;box-sizing:border-box;width:56px;height:56px;padding:0;border:none;fill:currentColor;text-decoration:none;cursor:pointer;user-select:none;-moz-appearance:none;-webkit-appearance:none;overflow:visible;transition:box-shadow 280ms cubic-bezier(0.4, 0, 0.2, 1),opacity 15ms linear 30ms,transform 270ms 0ms cubic-bezier(0, 0, 0.2, 1)}:host .mdc-fab .mdc-elevation-overlay{width:100%;height:100%;top:0;left:0}:host .mdc-fab::-moz-focus-inner{padding:0;border:0}:host .mdc-fab:hover{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12)}:host .mdc-fab.mdc-ripple-upgraded--background-focused,:host .mdc-fab:not(.mdc-ripple-upgraded):focus{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12)}:host .mdc-fab:active,:host .mdc-fab:focus:active{box-shadow:0px 7px 8px -4px rgba(0, 0, 0, 0.2),0px 12px 17px 2px rgba(0, 0, 0, 0.14),0px 5px 22px 4px rgba(0,0,0,.12)}:host .mdc-fab:active,:host .mdc-fab:focus{outline:none}:host .mdc-fab:hover{cursor:pointer}:host .mdc-fab>svg{width:100%}:host .mdc-fab--mini{width:40px;height:40px}:host .mdc-fab--extended{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-button-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-button-font-size, 0.875rem);line-height:2.25rem;line-height:var(--mdc-typography-button-line-height, 2.25rem);font-weight:500;font-weight:var(--mdc-typography-button-font-weight, 500);letter-spacing:0.0892857143em;letter-spacing:var(--mdc-typography-button-letter-spacing, 0.0892857143em);text-decoration:none;text-decoration:var(--mdc-typography-button-text-decoration, none);text-transform:uppercase;text-transform:var(--mdc-typography-button-text-transform, uppercase);border-radius:24px;padding-left:20px;padding-right:20px;width:auto;max-width:100%;height:48px;line-height:normal}:host .mdc-fab--extended .mdc-fab__ripple{border-radius:24px}:host .mdc-fab--extended .mdc-fab__icon{margin-left:calc(12px - 20px);margin-right:12px}[dir=rtl] :host .mdc-fab--extended .mdc-fab__icon,:host .mdc-fab--extended .mdc-fab__icon[dir=rtl]{margin-left:12px;margin-right:calc(12px - 20px)}:host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon{margin-left:12px;margin-right:calc(12px - 20px)}[dir=rtl] :host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon,:host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon[dir=rtl]{margin-left:calc(12px - 20px);margin-right:12px}:host .mdc-fab--touch{margin-top:4px;margin-bottom:4px;margin-right:4px;margin-left:4px}:host .mdc-fab--touch .mdc-fab__touch{position:absolute;top:50%;height:48px;left:50%;width:48px;transform:translate(-50%, -50%)}:host .mdc-fab::before{position:absolute;box-sizing:border-box;width:100%;height:100%;top:0;left:0;border:1px solid transparent;border-radius:inherit;content:"";pointer-events:none}:host .mdc-fab__label{justify-content:flex-start;text-overflow:ellipsis;white-space:nowrap;overflow-x:hidden;overflow-y:visible}:host .mdc-fab__icon{transition:transform 180ms 90ms cubic-bezier(0, 0, 0.2, 1);fill:currentColor;will-change:transform}:host .mdc-fab .mdc-fab__icon{display:inline-flex;align-items:center;justify-content:center}:host .mdc-fab--exited{transform:scale(0);opacity:0;transition:opacity 15ms linear 150ms,transform 180ms 0ms cubic-bezier(0.4, 0, 1, 1)}:host .mdc-fab--exited .mdc-fab__icon{transform:scale(0);transition:transform 135ms 0ms cubic-bezier(0.4, 0, 1, 1)}:host .mdc-fab{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);box-shadow:0px 3px 5px -1px rgba(0, 0, 0, 0.2),0px 6px 10px 0px rgba(0, 0, 0, 0.14),0px 1px 18px 0px rgba(0,0,0,.12)}:host .mdc-fab .mdc-fab__icon{width:24px;height:24px;font-size:24px}:host .mdc-fab,:host .mdc-fab:not(:disabled) .mdc-fab__icon,:host .mdc-fab:not(:disabled) .mdc-fab__label,:host .mdc-fab:disabled .mdc-fab__icon,:host .mdc-fab:disabled .mdc-fab__label{color:#fff;color:var(--mdc-theme-on-secondary, #fff)}:host .mdc-fab:not(.mdc-fab--extended){border-radius:50%}:host .mdc-fab:not(.mdc-fab--extended) .mdc-fab__ripple{border-radius:50%}:host .mdc-fab{position:relative;display:inline-flex;position:relative;align-items:center;justify-content:center;box-sizing:border-box;width:56px;height:56px;padding:0;border:none;fill:currentColor;text-decoration:none;cursor:pointer;user-select:none;-moz-appearance:none;-webkit-appearance:none;overflow:visible;transition:box-shadow 280ms cubic-bezier(0.4, 0, 0.2, 1),opacity 15ms linear 30ms,transform 270ms 0ms cubic-bezier(0, 0, 0.2, 1)}:host .mdc-fab .mdc-elevation-overlay{width:100%;height:100%;top:0;left:0}:host .mdc-fab::-moz-focus-inner{padding:0;border:0}:host .mdc-fab:hover{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12)}:host .mdc-fab.mdc-ripple-upgraded--background-focused,:host .mdc-fab:not(.mdc-ripple-upgraded):focus{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12)}:host .mdc-fab:active,:host .mdc-fab:focus:active{box-shadow:0px 7px 8px -4px rgba(0, 0, 0, 0.2),0px 12px 17px 2px rgba(0, 0, 0, 0.14),0px 5px 22px 4px rgba(0,0,0,.12)}:host .mdc-fab:active,:host .mdc-fab:focus{outline:none}:host .mdc-fab:hover{cursor:pointer}:host .mdc-fab>svg{width:100%}:host .mdc-fab--mini{width:40px;height:40px}:host .mdc-fab--extended{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-button-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-button-font-size, 0.875rem);line-height:2.25rem;line-height:var(--mdc-typography-button-line-height, 2.25rem);font-weight:500;font-weight:var(--mdc-typography-button-font-weight, 500);letter-spacing:0.0892857143em;letter-spacing:var(--mdc-typography-button-letter-spacing, 0.0892857143em);text-decoration:none;text-decoration:var(--mdc-typography-button-text-decoration, none);text-transform:uppercase;text-transform:var(--mdc-typography-button-text-transform, uppercase);border-radius:24px;padding-left:20px;padding-right:20px;width:auto;max-width:100%;height:48px;line-height:normal}:host .mdc-fab--extended .mdc-fab__ripple{border-radius:24px}:host .mdc-fab--extended .mdc-fab__icon{margin-left:calc(12px - 20px);margin-right:12px}[dir=rtl] :host .mdc-fab--extended .mdc-fab__icon,:host .mdc-fab--extended .mdc-fab__icon[dir=rtl]{margin-left:12px;margin-right:calc(12px - 20px)}:host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon{margin-left:12px;margin-right:calc(12px - 20px)}[dir=rtl] :host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon,:host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon[dir=rtl]{margin-left:calc(12px - 20px);margin-right:12px}:host .mdc-fab--touch{margin-top:4px;margin-bottom:4px;margin-right:4px;margin-left:4px}:host .mdc-fab--touch .mdc-fab__touch{position:absolute;top:50%;height:48px;left:50%;width:48px;transform:translate(-50%, -50%)}:host .mdc-fab::before{position:absolute;box-sizing:border-box;width:100%;height:100%;top:0;left:0;border:1px solid transparent;border-radius:inherit;content:"";pointer-events:none}:host .mdc-fab__label{justify-content:flex-start;text-overflow:ellipsis;white-space:nowrap;overflow-x:hidden;overflow-y:visible}:host .mdc-fab__icon{transition:transform 180ms 90ms cubic-bezier(0, 0, 0.2, 1);fill:currentColor;will-change:transform}:host .mdc-fab .mdc-fab__icon{display:inline-flex;align-items:center;justify-content:center}:host .mdc-fab--exited{transform:scale(0);opacity:0;transition:opacity 15ms linear 150ms,transform 180ms 0ms cubic-bezier(0.4, 0, 1, 1)}:host .mdc-fab--exited .mdc-fab__icon{transform:scale(0);transition:transform 135ms 0ms cubic-bezier(0.4, 0, 1, 1)}:host .mdc-fab .ripple{overflow:hidden}:host .mdc-fab:not(.mdc-fab--extended) .ripple{border-radius:50%}:host .mdc-fab .mdc-fab__label{z-index:0}:host .mdc-fab:not(.mdc-fab--extended) .ripple{border-radius:50%}:host .mdc-fab .mdc-fab__icon ::slotted(*){width:inherit;height:inherit;font-size:inherit}:host .mdc-fab--extended.mdc-fab--exited .mdc-fab__icon ::slotted(*){transform:scale(0);transition:transform 135ms 0ms cubic-bezier(0.4, 0, 1, 1)}:host .mdc-fab{padding-top:0px;padding-top:max(0px, var(--mdc-fab-focus-outline-width, 0px));padding-right:0px;padding-right:max(0px, var(--mdc-fab-focus-outline-width, 0px));padding-bottom:0px;padding-bottom:max(0px, var(--mdc-fab-focus-outline-width, 0px));padding-left:0px;padding-left:max(0px, var(--mdc-fab-focus-outline-width, 0px));box-shadow:0px 3px 5px -1px rgba(0, 0, 0, 0.2), 0px 6px 10px 0px rgba(0, 0, 0, 0.14), 0px 1px 18px 0px rgba(0, 0, 0, 0.12);box-shadow:var(--mdc-fab-box-shadow, 0px 3px 5px -1px rgba(0, 0, 0, 0.2), 0px 6px 10px 0px rgba(0, 0, 0, 0.14), 0px 1px 18px 0px rgba(0, 0, 0, 0.12))}:host .mdc-fab:not(:disabled).mdc-ripple-upgraded--background-focused,:host .mdc-fab:not(:disabled):not(.mdc-ripple-upgraded):focus{border-color:initial;border-color:var(--mdc-fab-focus-outline-color, initial)}:host .mdc-fab:not(:disabled).mdc-ripple-upgraded--background-focused,:host .mdc-fab:not(:disabled):not(.mdc-ripple-upgraded):focus{border-style:solid;border-width:var(--mdc-fab-focus-outline-width, 0px);padding-top:0px;padding-top:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-right:0px;padding-right:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-bottom:0px;padding-bottom:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-left:0px;padding-left:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1))}:host .mdc-fab:hover,:host .mdc-fab:focus{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2), 0px 8px 10px 1px rgba(0, 0, 0, 0.14), 0px 3px 14px 2px rgba(0, 0, 0, 0.12);box-shadow:var(--mdc-fab-box-shadow, 0px 5px 5px -3px rgba(0, 0, 0, 0.2), 0px 8px 10px 1px rgba(0, 0, 0, 0.14), 0px 3px 14px 2px rgba(0, 0, 0, 0.12))}:host .mdc-fab:active{box-shadow:0px 7px 8px -4px rgba(0, 0, 0, 0.2), 0px 12px 17px 2px rgba(0, 0, 0, 0.14), 0px 5px 22px 4px rgba(0, 0, 0, 0.12);box-shadow:var(--mdc-fab-box-shadow, 0px 7px 8px -4px rgba(0, 0, 0, 0.2), 0px 12px 17px 2px rgba(0, 0, 0, 0.14), 0px 5px 22px 4px rgba(0, 0, 0, 0.12))}:host .mdc-fab .ripple{overflow:hidden}:host .mdc-fab .mdc-fab__label{z-index:0}:host .mdc-fab:not(.mdc-fab--extended) .ripple{border-radius:50%}:host .mdc-fab.mdc-fab--extended .ripple{border-radius:24px}:host .mdc-fab .mdc-fab__icon{width:24px;width:var(--mdc-icon-size, 24px);height:24px;height:var(--mdc-icon-size, 24px);font-size:24px;font-size:var(--mdc-icon-size, 24px);transition:transform 180ms 90ms cubic-bezier(0, 0, 0.2, 1);fill:currentColor;will-change:transform;display:inline-flex;align-items:center;justify-content:center}:host .mdc-fab.mdc-fab--extended{padding-top:0px;padding-top:max(0px, var(--mdc-fab-focus-outline-width, 0px));padding-right:20px;padding-right:max(var(--mdc-fab-extended-label-padding, 20px), var(--mdc-fab-focus-outline-width, 0px));padding-bottom:0px;padding-bottom:max(0px, var(--mdc-fab-focus-outline-width, 0px));padding-left:20px;padding-left:max(var(--mdc-fab-extended-label-padding, 20px), var(--mdc-fab-focus-outline-width, 0px))}:host .mdc-fab.mdc-fab--extended:not(:disabled).mdc-ripple-upgraded--background-focused,:host .mdc-fab.mdc-fab--extended:not(:disabled):not(.mdc-ripple-upgraded):focus{border-style:solid;border-width:var(--mdc-fab-focus-outline-width, 0px);padding-top:0px;padding-top:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-right:20px;padding-right:max(calc(var(--mdc-fab-extended-label-padding, 20px) - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(var(--mdc-fab-extended-label-padding, 20px) - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-bottom:0px;padding-bottom:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-left:20px;padding-left:max(calc(var(--mdc-fab-extended-label-padding, 20px) - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(var(--mdc-fab-extended-label-padding, 20px) - var(--mdc-fab-focus-outline-width, 0px)) * -1))}:host .mdc-fab.mdc-fab--extended.icon-end .mdc-fab__icon{margin-left:12px;margin-left:var(--mdc-fab-extended-icon-padding, 12px);margin-right:calc(12px - 20px);margin-right:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px))}[dir=rtl] :host .mdc-fab.mdc-fab--extended.icon-end .mdc-fab__icon,:host .mdc-fab.mdc-fab--extended.icon-end .mdc-fab__icon[dir=rtl]{margin-left:calc(12px - 20px);margin-left:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px));margin-right:12px;margin-right:var(--mdc-fab-extended-icon-padding, 12px)}`;let it=class extends tt{};it.styles=[et],it=t([l("mwc-fab")],it),h([l("ha-fab")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"method",key:"firstUpdated",value:function(t){p(m(i.prototype),"firstUpdated",this).call(this,t),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}}]}}),it);const ot=t=>e=>({kind:"method",placement:"prototype",key:e.key,descriptor:{set(t){this["__"+String(e.key)]=t},get(){return this["__"+String(e.key)]},enumerable:!0,configurable:!0},finisher(i){const o=i.prototype.connectedCallback;i.prototype.connectedCallback=function(){if(o.call(this),this[e.key]){const i=this.renderRoot.querySelector(t);if(!i)return;i.scrollTop=this[e.key]}}}});h([l("ha-tab")],(function(t,a){return{F:class extends a{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"active",value:()=>!1},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[i()],key:"name",value:void 0},{kind:"field",decorators:[e("mwc-ripple")],key:"_ripple",value:void 0},{kind:"field",decorators:[o()],key:"_shouldRenderRipple",value:()=>!1},{kind:"method",key:"render",value:function(){return r`
      <div
        tabindex="0"
        role="tab"
        aria-selected=${this.active}
        aria-label=${u(this.name)}
        @focus=${this.handleRippleFocus}
        @blur=${this.handleRippleBlur}
        @mousedown=${this.handleRippleActivate}
        @mouseup=${this.handleRippleDeactivate}
        @mouseenter=${this.handleRippleMouseEnter}
        @mouseleave=${this.handleRippleMouseLeave}
        @touchstart=${this.handleRippleActivate}
        @touchend=${this.handleRippleDeactivate}
        @touchcancel=${this.handleRippleDeactivate}
        @keydown=${this._handleKeyDown}
      >
        ${this.narrow?r`<slot name="icon"></slot>`:""}
        ${!this.narrow||this.active?r`<span class="name">${this.name}</span>`:""}
        ${this._shouldRenderRipple?r`<mwc-ripple></mwc-ripple>`:""}
      </div>
    `}},{kind:"field",key:"_rippleHandlers",value(){return new n(()=>(this._shouldRenderRipple=!0,this._ripple))}},{kind:"method",key:"_handleKeyDown",value:function(t){13===t.keyCode&&t.target.click()}},{kind:"method",decorators:[s({passive:!0})],key:"handleRippleActivate",value:function(t){this._rippleHandlers.startPress(t)}},{kind:"method",key:"handleRippleDeactivate",value:function(){this._rippleHandlers.endPress()}},{kind:"method",key:"handleRippleMouseEnter",value:function(){this._rippleHandlers.startHover()}},{kind:"method",key:"handleRippleMouseLeave",value:function(){this._rippleHandlers.endHover()}},{kind:"method",key:"handleRippleFocus",value:function(){this._rippleHandlers.startFocus()}},{kind:"method",key:"handleRippleBlur",value:function(){this._rippleHandlers.endFocus()}},{kind:"get",static:!0,key:"styles",value:function(){return c`
      div {
        padding: 0 32px;
        display: flex;
        flex-direction: column;
        text-align: center;
        box-sizing: border-box;
        align-items: center;
        justify-content: center;
        height: var(--header-height);
        cursor: pointer;
        position: relative;
        outline: none;
      }

      .name {
        white-space: nowrap;
      }

      :host([active]) {
        color: var(--primary-color);
      }

      :host(:not([narrow])[active]) div {
        border-bottom: 2px solid var(--primary-color);
      }

      :host([narrow]) {
        min-width: 0;
        display: flex;
        justify-content: center;
        overflow: hidden;
      }
    `}}]}}),a),h([l("hass-tabs-subpage")],(function(t,e){class a extends e{constructor(...e){super(...e),t(this)}}return{F:a,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"supervisor",value:()=>!1},{kind:"field",decorators:[i({attribute:!1})],key:"localizeFunc",value:void 0},{kind:"field",decorators:[i({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[i()],key:"backCallback",value:void 0},{kind:"field",decorators:[i({type:Boolean,attribute:"main-page"})],key:"mainPage",value:()=>!1},{kind:"field",decorators:[i({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[i({type:Boolean,reflect:!0,attribute:"is-wide"})],key:"isWide",value:()=>!1},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"rtl",value:()=>!1},{kind:"field",decorators:[o()],key:"_activeTab",value:void 0},{kind:"field",decorators:[ot(".content")],key:"_savedScrollPos",value:void 0},{kind:"field",key:"_getTabs",value(){return f((t,e,i,o,s,a,n)=>t.filter(t=>(!t.component||t.core||q(this.hass,t.component))&&(!t.advancedOnly||i)).map(t=>r`
            <a href=${t.path}>
              <ha-tab
                .hass=${this.hass}
                .active=${t===e}
                .narrow=${this.narrow}
                .name=${t.translationKey?n(t.translationKey):t.name}
              >
                ${t.iconPath?r`<ha-svg-icon
                      slot="icon"
                      .path=${t.iconPath}
                    ></ha-svg-icon>`:r`<ha-icon slot="icon" .icon=${t.icon}></ha-icon>`}
              </ha-tab>
            </a>
          `))}},{kind:"method",key:"willUpdate",value:function(t){if(t.has("route")&&(this._activeTab=this.tabs.find(t=>`${this.route.prefix}${this.route.path}`.includes(t.path))),t.has("hass")){const e=t.get("hass");e&&e.language===this.hass.language||(this.rtl=W(this.hass))}p(m(a.prototype),"willUpdate",this).call(this,t)}},{kind:"method",key:"render",value:function(){var t,e;const i=this._getTabs(this.tabs,this._activeTab,null===(t=this.hass.userData)||void 0===t?void 0:t.showAdvanced,this.hass.config.components,this.hass.language,this.narrow,this.localizeFunc||this.hass.localize),o=i.length>1||!this.narrow;return r`
      <div class="toolbar">
        ${this.mainPage||!this.backPath&&null!==(e=history.state)&&void 0!==e&&e.root?r`
              <ha-menu-button
                .hassio=${this.supervisor}
                .hass=${this.hass}
                .narrow=${this.narrow}
              ></ha-menu-button>
            `:this.backPath?r`
              <a href=${this.backPath}>
                <ha-icon-button-arrow-prev
                  .hass=${this.hass}
                ></ha-icon-button-arrow-prev>
              </a>
            `:r`
              <ha-icon-button-arrow-prev
                .hass=${this.hass}
                @click=${this._backTapped}
              ></ha-icon-button-arrow-prev>
            `}
        ${this.narrow?r`<div class="main-title"><slot name="header"></slot></div>`:""}
        ${o?r`
              <div id="tabbar" class=${d({"bottom-bar":this.narrow})}>
                ${i}
              </div>
            `:""}
        <div id="toolbar-icon">
          <slot name="toolbar-icon"></slot>
        </div>
      </div>
      <div
        class="content ${d({tabs:o})}"
        @scroll=${this._saveScrollPos}
      >
        <slot></slot>
      </div>
      <div id="fab" class="${d({tabs:o})}">
        <slot name="fab"></slot>
      </div>
    `}},{kind:"method",decorators:[s({passive:!0})],key:"_saveScrollPos",value:function(t){this._savedScrollPos=t.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){this.backCallback?this.backCallback():history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return c`
      :host {
        display: block;
        height: 100%;
        background-color: var(--primary-background-color);
      }

      :host([narrow]) {
        width: 100%;
        position: fixed;
      }

      ha-menu-button {
        margin-right: 24px;
      }

      .toolbar {
        display: flex;
        align-items: center;
        font-size: 20px;
        height: var(--header-height);
        background-color: var(--sidebar-background-color);
        font-weight: 400;
        border-bottom: 1px solid var(--divider-color);
        padding: 0 16px;
        box-sizing: border-box;
      }
      .toolbar a {
        color: var(--sidebar-text-color);
        text-decoration: none;
      }
      .bottom-bar a {
        width: 25%;
      }

      #tabbar {
        display: flex;
        font-size: 14px;
      }

      #tabbar.bottom-bar {
        position: absolute;
        bottom: 0;
        left: 0;
        padding: 0 16px;
        box-sizing: border-box;
        background-color: var(--sidebar-background-color);
        border-top: 1px solid var(--divider-color);
        justify-content: space-around;
        z-index: 2;
        font-size: 12px;
        width: 100%;
        padding-bottom: env(safe-area-inset-bottom);
      }

      #tabbar:not(.bottom-bar) {
        flex: 1;
        justify-content: center;
      }

      :host(:not([narrow])) #toolbar-icon {
        min-width: 40px;
      }

      ha-menu-button,
      ha-icon-button-arrow-prev,
      ::slotted([slot="toolbar-icon"]) {
        flex-shrink: 0;
        pointer-events: auto;
        color: var(--sidebar-icon-color);
      }

      .main-title {
        flex: 1;
        max-height: var(--header-height);
        line-height: 20px;
        color: var(--sidebar-text-color);
      }

      .content {
        position: relative;
        width: calc(
          100% - env(safe-area-inset-left) - env(safe-area-inset-right)
        );
        margin-left: env(safe-area-inset-left);
        margin-right: env(safe-area-inset-right);
        height: calc(100% - 1px - var(--header-height));
        height: calc(
          100% - 1px - var(--header-height) - env(safe-area-inset-bottom)
        );
        overflow: auto;
        -webkit-overflow-scrolling: touch;
      }

      :host([narrow]) .content.tabs {
        height: calc(100% - 2 * var(--header-height));
        height: calc(
          100% - 2 * var(--header-height) - env(safe-area-inset-bottom)
        );
      }

      #fab {
        position: fixed;
        right: calc(16px + env(safe-area-inset-right));
        bottom: calc(16px + env(safe-area-inset-bottom));
        z-index: 1;
      }
      :host([narrow]) #fab.tabs {
        bottom: calc(84px + env(safe-area-inset-bottom));
      }
      #fab[is-wide] {
        bottom: 24px;
        right: 24px;
      }
      :host([rtl]) #fab {
        right: auto;
        left: calc(16px + env(safe-area-inset-left));
      }
      :host([rtl][is-wide]) #fab {
        bottom: 24px;
        left: 24px;
        right: auto;
      }
    `}}]}}),a),g({_template:b`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[Y]});h([l("hacs-repository-card")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"hacs",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"repository",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"status",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"removed",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"addedToLovelace",value:void 0},{kind:"get",key:"_borderClass",value:function(){const t={};return this.addedToLovelace&&"pending-restart"!==this.repository.status?this.repository.pending_upgrade?t["status-update"]=!0:this.repository.new&&!this.repository.installed&&(t["status-new"]=!0):t["status-issue"]=!0,0!==Object.keys(t).length&&(t["status-border"]=!0),t}},{kind:"get",key:"_headerClass",value:function(){const t={};return this.addedToLovelace&&"pending-restart"!==this.repository.status?this.repository.pending_upgrade?t["update-header"]=!0:this.repository.new&&!this.repository.installed?t["new-header"]=!0:t["default-header"]=!0:t["issue-header"]=!0,t}},{kind:"get",key:"_headerTitle",value:function(){return this.addedToLovelace?"pending-restart"===this.repository.status?this.hacs.localize("repository_card.pending_restart"):this.repository.pending_upgrade?this.hacs.localize("repository_card.pending_update"):this.repository.new&&!this.repository.installed?this.hacs.localize("repository_card.new_repository"):"":this.hacs.localize("repository_card.not_loaded")}},{kind:"method",key:"render",value:function(){const t=this.repository.local_path.split("/");return r`
      <ha-card class=${d(this._borderClass)} ?narrow=${this.narrow}>
        <div class="card-content">
          <div class="group-header">
            <div class="status-header ${d(this._headerClass)}">${this._headerTitle}</div>
            <div class="title">
              <h1 class="pointer" @click=${this._showReopsitoryInfo}>${this.repository.name}</h1>
              ${"integration"!==this.repository.category?r` <hacs-chip
                    .icon=${V}
                    .value=${this.hacs.localize("common."+this.repository.category)}
                  ></hacs-chip>`:""}
            </div>
          </div>
          <paper-item>
            <paper-item-body>${this.repository.description}</paper-item-body></paper-item
          >
        </div>
        <div class="card-actions">
          ${this.repository.new&&!this.repository.installed?r`<div>
                  <mwc-button @click=${this._installRepository}
                    >${this.hacs.localize("common.install")}</mwc-button
                  >
                </div>
                <div>
                  <mwc-button @click=${this._showReopsitoryInfo}
                    >${this.hacs.localize("repository_card.information")}</mwc-button
                  >
                </div>
                <div>
                  <hacs-link .url="https://github.com/${this.repository.full_name}"
                    ><mwc-button>${this.hacs.localize("common.repository")}</mwc-button></hacs-link
                  >
                </div>
                <div>
                  <mwc-button @click=${this._setNotNew}
                    >${this.hacs.localize("repository_card.dismiss")}</mwc-button
                  >
                </div>`:this.repository.pending_upgrade&&this.addedToLovelace?r`<div>
                  <mwc-button class="update-header" @click=${this._updateRepository} raised
                    >${this.hacs.localize("common.update")}</mwc-button
                  >
                </div>
                <div>
                  <hacs-link .url="https://github.com/${this.repository.full_name}"
                    ><mwc-button>${this.hacs.localize("common.repository")}</mwc-button></hacs-link
                  >
                </div>`:r`<div>
                <hacs-link .url="https://github.com/${this.repository.full_name}"
                  ><mwc-button>${this.hacs.localize("common.repository")}</mwc-button></hacs-link
                >
              </div>`}
          ${this.repository.installed?r` <paper-menu-button
                horizontal-align="right"
                vertical-align="top"
                vertical-offset="40"
                close-on-activate
              >
                <mwc-icon-button slot="dropdown-trigger" alt="menu">
                  <ha-svg-icon .path=${x}></ha-svg-icon>
                </mwc-icon-button>
                <paper-listbox slot="dropdown-content">
                  <paper-item class="pointer" @tap=${this._showReopsitoryInfo}
                    >${this.hacs.localize("repository_card.information")}</paper-item
                  >

                  <paper-item class="pointer" @tap=${this._updateReopsitoryInfo}
                    >${this.hacs.localize("repository_card.update_information")}</paper-item
                  >

                  <paper-item @tap=${this._installRepository}
                    >${this.hacs.localize("repository_card.reinstall")}</paper-item
                  >

                  ${"plugin"===this.repository.category?r`<hacs-link
                        .url="/hacsfiles/${t.pop()}/${this.repository.file_name}"
                        newtab
                        ><paper-item class="pointer"
                          >${this.hacs.localize("repository_card.open_source")}</paper-item
                        ></hacs-link
                      >`:""}

                  <hacs-link .url="https://github.com/${this.repository.full_name}/issues"
                    ><paper-item class="pointer"
                      >${this.hacs.localize("repository_card.open_issue")}</paper-item
                    ></hacs-link
                  >

                  ${"172733314"!==String(this.repository.id)?r`<hacs-link
                          .url="https://github.com/hacs/integration/issues/new?assignees=ludeeus&labels=flag&template=removal.yml&repo=${this.repository.full_name}&title=Request for removal of ${this.repository.full_name}"
                          ><paper-item class="pointer uninstall"
                            >${this.hacs.localize("repository_card.report")}</paper-item
                          ></hacs-link
                        >
                        <paper-item
                          class="pointer uninstall"
                          @tap=${this._uninstallRepositoryDialog}
                          >${this.hacs.localize("common.uninstall")}</paper-item
                        >`:""}
                </paper-listbox>
              </paper-menu-button>`:""}
        </div>
      </ha-card>
    `}},{kind:"method",key:"_updateReopsitoryInfo",value:async function(){await v(this.hass,this.repository.id)}},{kind:"method",key:"_showReopsitoryInfo",value:async function(){this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"repository-info",repository:this.repository.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_updateRepository",value:async function(){this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"update",repository:this.repository.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_setNotNew",value:async function(){await y(this.hass,this.repository.id)}},{kind:"method",key:"_installRepository",value:function(){this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"install",repository:this.repository.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_uninstallRepositoryDialog",value:async function(){if("integration"===this.repository.category&&this.repository.config_flow){if((await(t=this.hass,t.callApi("GET","config/config_entries/entry"))).some(t=>t.domain===this.repository.domain))return void await J(this,{title:this.hacs.localize("dialog.configured.title"),text:this.hacs.localize("dialog.configured.message",{name:this.repository.name}),confirmText:this.hacs.localize("dialog.configured.confirm"),confirm:()=>{_("/config/integrations",{replace:!0})}})}var t;this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"progress",title:this.hacs.localize("dialog.uninstall.title"),confirmText:this.hacs.localize("dialog.uninstall.title"),content:this.hacs.localize("dialog.uninstall.message",{name:this.repository.name}),confirm:async()=>{await this._uninstallRepository()}},bubbles:!0,composed:!0}))}},{kind:"method",key:"_uninstallRepository",value:async function(){var t;if("plugin"===this.repository.category&&"yaml"!==(null===(t=this.hacs.status)||void 0===t?void 0:t.lovelace_mode)){const t=await w(this.hass),e=I({repository:this.repository,skipTag:!0});await Promise.all(t.filter(t=>t.url.includes(e)).map(t=>E(this.hass,String(t.id))))}await k(this.hass,this.repository.id)}},{kind:"get",static:!0,key:"styles",value:function(){return[T,c`
        ha-card {
          display: flex;
          flex-direction: column;
          height: 100%;
          width: 480px;
          border-style: solid;
          border-width: min(var(--ha-card-border-width, 1px), 10px);
          border-color: transparent;
          border-radius: var(--ha-card-border-radius, 4px);
        }

        hacs-chip {
          margin: 8px 4px 0 0;
        }
        .title {
          display: flex;
          justify-content: space-between;
        }
        .card-content {
          padding: 0 0 3px 0;
          height: 100%;
        }
        .card-actions {
          border-top: none;
          bottom: 0;
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 5px;
        }
        .group-header {
          height: auto;
          align-content: center;
        }
        .group-header h1 {
          margin: 0;
          padding: 8px 16px;
        }
        h1 {
          margin-top: 0;
          min-height: 24px;
        }
        paper-menu-button {
          padding: 0;
          float: right;
        }

        .pointer {
          cursor: pointer;
        }
        paper-item-body {
          opacity: var(--dark-primary-opacity);
        }

        .status-new {
          border-color: var(--hcv-color-new);
        }

        .status-update {
          border-color: var(--hcv-color-update);
        }

        .status-issue {
          border-color: var(--hcv-color-error);
        }

        .new-header {
          background-color: var(--hcv-color-new);
          color: var(--hcv-text-color-on-background);
        }

        .issue-header {
          background-color: var(--hcv-color-error);
          color: var(--hcv-text-color-on-background);
        }

        .update-header {
          background-color: var(--hcv-color-update);
          color: var(--hcv-text-color-on-background);
        }

        .default-header {
          padding: 10px 0 !important;
        }

        mwc-button.update-header {
          --mdc-theme-primary: var(--hcv-color-update);
          --mdc-theme-on-primary: var(--hcv-text-color-on-background);
        }

        .status-border {
          border-style: solid;
          border-width: min(var(--ha-card-border-width, 1px), 10px);
        }

        .status-header {
          top: 0;
          padding: 6px 1px;
          margin: -1px;
          width: 100%;
          font-weight: 300;
          text-align: center;
          left: 0;
          border-top-left-radius: var(--ha-card-border-radius, 4px);
          border-top-right-radius: var(--ha-card-border-radius, 4px);
        }

        ha-card[narrow] {
          width: calc(100% - 24px);
          margin: 11px;
        }
      `]}}]}}),a);class st extends a{constructor(){super(...arguments),this.value="",this.group=null,this.tabindex=-1,this.disabled=!1,this.twoline=!1,this.activated=!1,this.graphic=null,this.multipleGraphics=!1,this.hasMeta=!1,this.noninteractive=!1,this.selected=!1,this.shouldRenderRipple=!1,this._managingList=null,this.boundOnClick=this.onClick.bind(this),this._firstChanged=!0,this._skipPropRequest=!1,this.rippleHandlers=new n(()=>(this.shouldRenderRipple=!0,this.ripple)),this.listeners=[{target:this,eventNames:["click"],cb:()=>{this.onClick()}},{target:this,eventNames:["mouseenter"],cb:this.rippleHandlers.startHover},{target:this,eventNames:["mouseleave"],cb:this.rippleHandlers.endHover},{target:this,eventNames:["focus"],cb:this.rippleHandlers.startFocus},{target:this,eventNames:["blur"],cb:this.rippleHandlers.endFocus},{target:this,eventNames:["mousedown","touchstart"],cb:t=>{const e=t.type;this.onDown("mousedown"===e?"mouseup":"touchend",t)}}]}get text(){const t=this.textContent;return t?t.trim():""}render(){const t=this.renderText(),e=this.graphic?this.renderGraphic():r``,i=this.hasMeta?this.renderMeta():r``;return r`
      ${this.renderRipple()}
      ${e}
      ${t}
      ${i}`}renderRipple(){return this.shouldRenderRipple?r`
      <mwc-ripple
        .activated=${this.activated}>
      </mwc-ripple>`:this.activated?r`<div class="fake-activated-ripple"></div>`:""}renderGraphic(){const t={multi:this.multipleGraphics};return r`
      <span class="mdc-deprecated-list-item__graphic material-icons ${d(t)}">
        <slot name="graphic"></slot>
      </span>`}renderMeta(){return r`
      <span class="mdc-deprecated-list-item__meta material-icons">
        <slot name="meta"></slot>
      </span>`}renderText(){const t=this.twoline?this.renderTwoline():this.renderSingleLine();return r`
      <span class="mdc-deprecated-list-item__text">
        ${t}
      </span>`}renderSingleLine(){return r`<slot></slot>`}renderTwoline(){return r`
      <span class="mdc-deprecated-list-item__primary-text">
        <slot></slot>
      </span>
      <span class="mdc-deprecated-list-item__secondary-text">
        <slot name="secondary"></slot>
      </span>
    `}onClick(){this.fireRequestSelected(!this.selected,"interaction")}onDown(t,e){const i=()=>{window.removeEventListener(t,i),this.rippleHandlers.endPress()};window.addEventListener(t,i),this.rippleHandlers.startPress(e)}fireRequestSelected(t,e){if(this.noninteractive)return;const i=new CustomEvent("request-selected",{bubbles:!0,composed:!0,detail:{source:e,selected:t}});this.dispatchEvent(i)}connectedCallback(){super.connectedCallback(),this.noninteractive||this.setAttribute("mwc-list-item","");for(const t of this.listeners)for(const e of t.eventNames)t.target.addEventListener(e,t.cb,{passive:!0})}disconnectedCallback(){super.disconnectedCallback();for(const t of this.listeners)for(const e of t.eventNames)t.target.removeEventListener(e,t.cb);this._managingList&&(this._managingList.debouncedLayout?this._managingList.debouncedLayout(!0):this._managingList.layout(!0))}firstUpdated(){const t=new Event("list-item-rendered",{bubbles:!0,composed:!0});this.dispatchEvent(t)}}t([R("slot")],st.prototype,"slotElement",void 0),t([e("mwc-ripple")],st.prototype,"ripple",void 0),t([i({type:String})],st.prototype,"value",void 0),t([i({type:String,reflect:!0})],st.prototype,"group",void 0),t([i({type:Number,reflect:!0})],st.prototype,"tabindex",void 0),t([i({type:Boolean,reflect:!0}),Q((function(t){t?this.setAttribute("aria-disabled","true"):this.setAttribute("aria-disabled","false")}))],st.prototype,"disabled",void 0),t([i({type:Boolean,reflect:!0})],st.prototype,"twoline",void 0),t([i({type:Boolean,reflect:!0})],st.prototype,"activated",void 0),t([i({type:String,reflect:!0})],st.prototype,"graphic",void 0),t([i({type:Boolean})],st.prototype,"multipleGraphics",void 0),t([i({type:Boolean})],st.prototype,"hasMeta",void 0),t([i({type:Boolean,reflect:!0}),Q((function(t){t?(this.removeAttribute("aria-checked"),this.removeAttribute("mwc-list-item"),this.selected=!1,this.activated=!1,this.tabIndex=-1):this.setAttribute("mwc-list-item","")}))],st.prototype,"noninteractive",void 0),t([i({type:Boolean,reflect:!0}),Q((function(t){const e=this.getAttribute("role"),i="gridcell"===e||"option"===e||"row"===e||"tab"===e;i&&t?this.setAttribute("aria-selected","true"):i&&this.setAttribute("aria-selected","false"),this._firstChanged?this._firstChanged=!1:this._skipPropRequest||this.fireRequestSelected(t,"property")}))],st.prototype,"selected",void 0),t([o()],st.prototype,"shouldRenderRipple",void 0),t([o()],st.prototype,"_managingList",void 0);const at=c`:host{cursor:pointer;user-select:none;-webkit-tap-highlight-color:transparent;height:48px;display:flex;position:relative;align-items:center;justify-content:flex-start;overflow:hidden;padding:0;padding-left:var(--mdc-list-side-padding, 16px);padding-right:var(--mdc-list-side-padding, 16px);outline:none;height:48px;color:rgba(0,0,0,.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host:focus{outline:none}:host([activated]){color:#6200ee;color:var(--mdc-theme-primary, #6200ee);--mdc-ripple-color: var( --mdc-theme-primary, #6200ee )}:host([activated]) .mdc-deprecated-list-item__graphic{color:#6200ee;color:var(--mdc-theme-primary, #6200ee)}:host([activated]) .fake-activated-ripple::before{position:absolute;display:block;top:0;bottom:0;left:0;right:0;width:100%;height:100%;pointer-events:none;z-index:1;content:"";opacity:0.12;opacity:var(--mdc-ripple-activated-opacity, 0.12);background-color:#6200ee;background-color:var(--mdc-ripple-color, var(--mdc-theme-primary, #6200ee))}.mdc-deprecated-list-item__graphic{flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;display:inline-flex}.mdc-deprecated-list-item__graphic ::slotted(*){flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;width:100%;height:100%;text-align:center}.mdc-deprecated-list-item__meta{width:var(--mdc-list-item-meta-size, 24px);height:var(--mdc-list-item-meta-size, 24px);margin-left:auto;margin-right:0;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-hint-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-item__meta.multi{width:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:var(--mdc-list-item-meta-size, 24px);line-height:var(--mdc-list-item-meta-size, 24px)}.mdc-deprecated-list-item__meta ::slotted(.material-icons),.mdc-deprecated-list-item__meta ::slotted(mwc-icon){line-height:var(--mdc-list-item-meta-size, 24px) !important}.mdc-deprecated-list-item__meta ::slotted(:not(.material-icons):not(mwc-icon)){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-caption-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.75rem;font-size:var(--mdc-typography-caption-font-size, 0.75rem);line-height:1.25rem;line-height:var(--mdc-typography-caption-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-caption-font-weight, 400);letter-spacing:0.0333333333em;letter-spacing:var(--mdc-typography-caption-letter-spacing, 0.0333333333em);text-decoration:inherit;text-decoration:var(--mdc-typography-caption-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-caption-text-transform, inherit)}[dir=rtl] .mdc-deprecated-list-item__meta,.mdc-deprecated-list-item__meta[dir=rtl]{margin-left:0;margin-right:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:100%;height:100%}.mdc-deprecated-list-item__text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden}.mdc-deprecated-list-item__text ::slotted([for]),.mdc-deprecated-list-item__text[for]{pointer-events:none}.mdc-deprecated-list-item__primary-text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;margin-bottom:-20px;display:block}.mdc-deprecated-list-item__primary-text::before{display:inline-block;width:0;height:32px;content:"";vertical-align:0}.mdc-deprecated-list-item__primary-text::after{display:inline-block;width:0;height:20px;content:"";vertical-align:-20px}.mdc-deprecated-list-item__secondary-text{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;display:block}.mdc-deprecated-list-item__secondary-text::before{display:inline-block;width:0;height:20px;content:"";vertical-align:0}.mdc-deprecated-list--dense .mdc-deprecated-list-item__secondary-text{font-size:inherit}* ::slotted(a),a{color:inherit;text-decoration:none}:host([twoline]){height:72px}:host([twoline]) .mdc-deprecated-list-item__text{align-self:flex-start}:host([disabled]),:host([noninteractive]){cursor:default;pointer-events:none}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*){opacity:.38}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__primary-text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__secondary-text ::slotted(*){color:#000;color:var(--mdc-theme-on-surface, #000)}.mdc-deprecated-list-item__secondary-text ::slotted(*){color:rgba(0, 0, 0, 0.54);color:var(--mdc-theme-text-secondary-on-background, rgba(0, 0, 0, 0.54))}.mdc-deprecated-list-item__graphic ::slotted(*){background-color:transparent;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-icon-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-group__subheader ::slotted(*){color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 40px);height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 40px);line-height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 40px) !important}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){border-radius:50%}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic,:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic,:host([graphic=control]) .mdc-deprecated-list-item__graphic{margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 16px)}[dir=rtl] :host([graphic=avatar]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=medium]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=large]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=control]) .mdc-deprecated-list-item__graphic,:host([graphic=avatar]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=medium]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=large]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=control]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 16px);margin-right:0}:host([graphic=icon]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 24px);height:var(--mdc-list-item-graphic-size, 24px);margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 32px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 24px);line-height:var(--mdc-list-item-graphic-size, 24px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 24px) !important}[dir=rtl] :host([graphic=icon]) .mdc-deprecated-list-item__graphic,:host([graphic=icon]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 32px);margin-right:0}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:56px}:host([graphic=medium]:not([twoLine])),:host([graphic=large]:not([twoLine])){height:72px}:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 56px);height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic.multi,:host([graphic=large]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(*),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 56px);line-height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 56px) !important}:host([graphic=large]){padding-left:0px}`;let nt=class extends st{};nt.styles=[at],nt=t([l("mwc-list-item")],nt);var rt="Unknown",dt="Backspace",ct="Enter",lt="Spacebar",ht="PageUp",pt="PageDown",mt="End",ut="Home",ft="ArrowLeft",gt="ArrowUp",bt="ArrowRight",xt="ArrowDown",vt="Delete",yt="Escape",_t="Tab",wt=new Set;wt.add(dt),wt.add(ct),wt.add(lt),wt.add(ht),wt.add(pt),wt.add(mt),wt.add(ut),wt.add(ft),wt.add(gt),wt.add(bt),wt.add(xt),wt.add(vt),wt.add(yt),wt.add(_t);var It=8,Et=13,kt=32,Tt=33,Rt=34,At=35,Ct=36,St=37,Ot=38,Ft=39,$t=40,zt=46,Lt=27,Mt=9,Bt=new Map;Bt.set(It,dt),Bt.set(Et,ct),Bt.set(kt,lt),Bt.set(Tt,ht),Bt.set(Rt,pt),Bt.set(At,mt),Bt.set(Ct,ut),Bt.set(St,ft),Bt.set(Ot,gt),Bt.set(Ft,bt),Bt.set($t,xt),Bt.set(zt,vt),Bt.set(Lt,yt),Bt.set(Mt,_t);var Nt,Dt,Pt=new Set;function Ht(t){var e=t.key;if(wt.has(e))return e;var i=Bt.get(t.keyCode);return i||rt}Pt.add(ht),Pt.add(pt),Pt.add(mt),Pt.add(ut),Pt.add(ft),Pt.add(gt),Pt.add(bt),Pt.add(xt);var Ut="mdc-list-item--activated",jt="mdc-list-item",Gt="mdc-list-item--disabled",Vt="mdc-list-item--selected",Kt="mdc-list-item__text",qt="mdc-list-item__primary-text",Xt="mdc-list";(Nt={})[""+Ut]="mdc-list-item--activated",Nt[""+jt]="mdc-list-item",Nt[""+Gt]="mdc-list-item--disabled",Nt[""+Vt]="mdc-list-item--selected",Nt[""+qt]="mdc-list-item__primary-text",Nt[""+Xt]="mdc-list";var Wt=((Dt={})[""+Ut]="mdc-deprecated-list-item--activated",Dt[""+jt]="mdc-deprecated-list-item",Dt[""+Gt]="mdc-deprecated-list-item--disabled",Dt[""+Vt]="mdc-deprecated-list-item--selected",Dt[""+Kt]="mdc-deprecated-list-item__text",Dt[""+qt]="mdc-deprecated-list-item__primary-text",Dt[""+Xt]="mdc-deprecated-list",Dt),Qt={ACTION_EVENT:"MDCList:action",ARIA_CHECKED:"aria-checked",ARIA_CHECKED_CHECKBOX_SELECTOR:'[role="checkbox"][aria-checked="true"]',ARIA_CHECKED_RADIO_SELECTOR:'[role="radio"][aria-checked="true"]',ARIA_CURRENT:"aria-current",ARIA_DISABLED:"aria-disabled",ARIA_ORIENTATION:"aria-orientation",ARIA_ORIENTATION_HORIZONTAL:"horizontal",ARIA_ROLE_CHECKBOX_SELECTOR:'[role="checkbox"]',ARIA_SELECTED:"aria-selected",ARIA_INTERACTIVE_ROLES_SELECTOR:'[role="listbox"], [role="menu"]',ARIA_MULTI_SELECTABLE_SELECTOR:'[aria-multiselectable="true"]',CHECKBOX_RADIO_SELECTOR:'input[type="checkbox"], input[type="radio"]',CHECKBOX_SELECTOR:'input[type="checkbox"]',CHILD_ELEMENTS_TO_TOGGLE_TABINDEX:"\n    ."+jt+" button:not(:disabled),\n    ."+jt+" a,\n    ."+Wt[jt]+" button:not(:disabled),\n    ."+Wt[jt]+" a\n  ",DEPRECATED_SELECTOR:".mdc-deprecated-list",FOCUSABLE_CHILD_ELEMENTS:"\n    ."+jt+" button:not(:disabled),\n    ."+jt+" a,\n    ."+jt+' input[type="radio"]:not(:disabled),\n    .'+jt+' input[type="checkbox"]:not(:disabled),\n    .'+Wt[jt]+" button:not(:disabled),\n    ."+Wt[jt]+" a,\n    ."+Wt[jt]+' input[type="radio"]:not(:disabled),\n    .'+Wt[jt]+' input[type="checkbox"]:not(:disabled)\n  ',RADIO_SELECTOR:'input[type="radio"]',SELECTED_ITEM_SELECTOR:'[aria-selected="true"], [aria-current="true"]'},Yt={UNSET_INDEX:-1,TYPEAHEAD_BUFFER_CLEAR_TIMEOUT_MS:300};const Jt=(t,e)=>t-e,Zt=["input","button","textarea","select"];function te(t){return t instanceof Set}const ee=t=>{const e=t===Yt.UNSET_INDEX?new Set:t;return te(e)?new Set(e):new Set([e])};class ie extends A{constructor(t){super(Object.assign(Object.assign({},ie.defaultAdapter),t)),this.isMulti_=!1,this.wrapFocus_=!1,this.isVertical_=!0,this.selectedIndex_=Yt.UNSET_INDEX,this.focusedItemIndex_=Yt.UNSET_INDEX,this.useActivatedClass_=!1,this.ariaCurrentAttrValue_=null}static get strings(){return Qt}static get numbers(){return Yt}static get defaultAdapter(){return{focusItemAtIndex:()=>{},getFocusedElementIndex:()=>0,getListItemCount:()=>0,isFocusInsideList:()=>!1,isRootFocused:()=>!1,notifyAction:()=>{},notifySelected:()=>{},getSelectedStateForElementIndex:()=>!1,setDisabledStateForElementIndex:()=>{},getDisabledStateForElementIndex:()=>!1,setSelectedStateForElementIndex:()=>{},setActivatedStateForElementIndex:()=>{},setTabIndexForElementIndex:()=>{},setAttributeForElementIndex:()=>{},getAttributeForElementIndex:()=>null}}setWrapFocus(t){this.wrapFocus_=t}setMulti(t){this.isMulti_=t;const e=this.selectedIndex_;if(t){if(!te(e)){const t=e===Yt.UNSET_INDEX;this.selectedIndex_=t?new Set:new Set([e])}}else if(te(e))if(e.size){const t=Array.from(e).sort(Jt);this.selectedIndex_=t[0]}else this.selectedIndex_=Yt.UNSET_INDEX}setVerticalOrientation(t){this.isVertical_=t}setUseActivatedClass(t){this.useActivatedClass_=t}getSelectedIndex(){return this.selectedIndex_}setSelectedIndex(t){this.isIndexValid_(t)&&(this.isMulti_?this.setMultiSelectionAtIndex_(ee(t)):this.setSingleSelectionAtIndex_(t))}handleFocusIn(t,e){e>=0&&this.adapter.setTabIndexForElementIndex(e,0)}handleFocusOut(t,e){e>=0&&this.adapter.setTabIndexForElementIndex(e,-1),setTimeout(()=>{this.adapter.isFocusInsideList()||this.setTabindexToFirstSelectedItem_()},0)}handleKeydown(t,e,i){const o="ArrowLeft"===Ht(t),s="ArrowUp"===Ht(t),a="ArrowRight"===Ht(t),n="ArrowDown"===Ht(t),r="Home"===Ht(t),d="End"===Ht(t),c="Enter"===Ht(t),l="Spacebar"===Ht(t);if(this.adapter.isRootFocused())return void(s||d?(t.preventDefault(),this.focusLastElement()):(n||r)&&(t.preventDefault(),this.focusFirstElement()));let h,p=this.adapter.getFocusedElementIndex();if(!(-1===p&&(p=i,p<0))){if(this.isVertical_&&n||!this.isVertical_&&a)this.preventDefaultEvent(t),h=this.focusNextElement(p);else if(this.isVertical_&&s||!this.isVertical_&&o)this.preventDefaultEvent(t),h=this.focusPrevElement(p);else if(r)this.preventDefaultEvent(t),h=this.focusFirstElement();else if(d)this.preventDefaultEvent(t),h=this.focusLastElement();else if((c||l)&&e){const e=t.target;if(e&&"A"===e.tagName&&c)return;this.preventDefaultEvent(t),this.setSelectedIndexOnAction_(p,!0)}this.focusedItemIndex_=p,void 0!==h&&(this.setTabindexAtIndex_(h),this.focusedItemIndex_=h)}}handleSingleSelection(t,e,i){t!==Yt.UNSET_INDEX&&(this.setSelectedIndexOnAction_(t,e,i),this.setTabindexAtIndex_(t),this.focusedItemIndex_=t)}focusNextElement(t){let e=t+1;if(e>=this.adapter.getListItemCount()){if(!this.wrapFocus_)return t;e=0}return this.adapter.focusItemAtIndex(e),e}focusPrevElement(t){let e=t-1;if(e<0){if(!this.wrapFocus_)return t;e=this.adapter.getListItemCount()-1}return this.adapter.focusItemAtIndex(e),e}focusFirstElement(){return this.adapter.focusItemAtIndex(0),0}focusLastElement(){const t=this.adapter.getListItemCount()-1;return this.adapter.focusItemAtIndex(t),t}setEnabled(t,e){this.isIndexValid_(t)&&this.adapter.setDisabledStateForElementIndex(t,!e)}preventDefaultEvent(t){const e=(""+t.target.tagName).toLowerCase();-1===Zt.indexOf(e)&&t.preventDefault()}setSingleSelectionAtIndex_(t,e=!0){this.selectedIndex_!==t&&(this.selectedIndex_!==Yt.UNSET_INDEX&&(this.adapter.setSelectedStateForElementIndex(this.selectedIndex_,!1),this.useActivatedClass_&&this.adapter.setActivatedStateForElementIndex(this.selectedIndex_,!1)),e&&this.adapter.setSelectedStateForElementIndex(t,!0),this.useActivatedClass_&&this.adapter.setActivatedStateForElementIndex(t,!0),this.setAriaForSingleSelectionAtIndex_(t),this.selectedIndex_=t,this.adapter.notifySelected(t))}setMultiSelectionAtIndex_(t,e=!0){const i=((t,e)=>{const i=Array.from(t),o=Array.from(e),s={added:[],removed:[]},a=i.sort(Jt),n=o.sort(Jt);let r=0,d=0;for(;r<a.length||d<n.length;){const t=a[r],e=n[d];t!==e?void 0!==t&&(void 0===e||t<e)?(s.removed.push(t),r++):void 0!==e&&(void 0===t||e<t)&&(s.added.push(e),d++):(r++,d++)}return s})(ee(this.selectedIndex_),t);if(i.removed.length||i.added.length){for(const t of i.removed)e&&this.adapter.setSelectedStateForElementIndex(t,!1),this.useActivatedClass_&&this.adapter.setActivatedStateForElementIndex(t,!1);for(const t of i.added)e&&this.adapter.setSelectedStateForElementIndex(t,!0),this.useActivatedClass_&&this.adapter.setActivatedStateForElementIndex(t,!0);this.selectedIndex_=t,this.adapter.notifySelected(t,i)}}setAriaForSingleSelectionAtIndex_(t){this.selectedIndex_===Yt.UNSET_INDEX&&(this.ariaCurrentAttrValue_=this.adapter.getAttributeForElementIndex(t,Qt.ARIA_CURRENT));const e=null!==this.ariaCurrentAttrValue_,i=e?Qt.ARIA_CURRENT:Qt.ARIA_SELECTED;this.selectedIndex_!==Yt.UNSET_INDEX&&this.adapter.setAttributeForElementIndex(this.selectedIndex_,i,"false");const o=e?this.ariaCurrentAttrValue_:"true";this.adapter.setAttributeForElementIndex(t,i,o)}setTabindexAtIndex_(t){this.focusedItemIndex_===Yt.UNSET_INDEX&&0!==t?this.adapter.setTabIndexForElementIndex(0,-1):this.focusedItemIndex_>=0&&this.focusedItemIndex_!==t&&this.adapter.setTabIndexForElementIndex(this.focusedItemIndex_,-1),this.adapter.setTabIndexForElementIndex(t,0)}setTabindexToFirstSelectedItem_(){let t=0;"number"==typeof this.selectedIndex_&&this.selectedIndex_!==Yt.UNSET_INDEX?t=this.selectedIndex_:te(this.selectedIndex_)&&this.selectedIndex_.size>0&&(t=Math.min(...this.selectedIndex_)),this.setTabindexAtIndex_(t)}isIndexValid_(t){if(t instanceof Set){if(!this.isMulti_)throw new Error("MDCListFoundation: Array of index is only supported for checkbox based list");if(0===t.size)return!0;{let e=!1;for(const i of t)if(e=this.isIndexInRange_(i),e)break;return e}}if("number"==typeof t){if(this.isMulti_)throw new Error("MDCListFoundation: Expected array of index for checkbox based list but got number: "+t);return t===Yt.UNSET_INDEX||this.isIndexInRange_(t)}return!1}isIndexInRange_(t){const e=this.adapter.getListItemCount();return t>=0&&t<e}setSelectedIndexOnAction_(t,e,i){if(this.adapter.getDisabledStateForElementIndex(t))return;let o=t;if(this.isMulti_&&(o=new Set([t])),this.isIndexValid_(o)){if(this.isMulti_)this.toggleMultiAtIndex(t,i,e);else if(e||i)this.setSingleSelectionAtIndex_(t,e);else{this.selectedIndex_===t&&this.setSingleSelectionAtIndex_(Yt.UNSET_INDEX)}e&&this.adapter.notifyAction(t)}}toggleMultiAtIndex(t,e,i=!0){let o=!1;o=void 0===e?!this.adapter.getSelectedStateForElementIndex(t):e;const s=ee(this.selectedIndex_);o?s.add(t):s.delete(t),this.setMultiSelectionAtIndex_(s,i)}}const oe=t=>t.hasAttribute("mwc-list-item");function se(){const t=this.itemsReadyResolver;this.itemsReady=new Promise(t=>this.itemsReadyResolver=t),t()}class ae extends C{constructor(){super(),this.mdcAdapter=null,this.mdcFoundationClass=ie,this.activatable=!1,this.multi=!1,this.wrapFocus=!1,this.itemRoles=null,this.innerRole=null,this.innerAriaLabel=null,this.rootTabbable=!1,this.previousTabindex=null,this.noninteractive=!1,this.itemsReadyResolver=()=>{},this.itemsReady=Promise.resolve([]),this.items_=[];const t=function(t,e=50){let i;return function(o=!0){clearTimeout(i),i=setTimeout(()=>{t(o)},e)}}(this.layout.bind(this));this.debouncedLayout=(e=!0)=>{se.call(this),t(e)}}async getUpdateComplete(){const t=await super.getUpdateComplete();return await this.itemsReady,t}get items(){return this.items_}updateItems(){var t;const e=null!==(t=this.assignedElements)&&void 0!==t?t:[],i=[];for(const t of e)oe(t)&&(i.push(t),t._managingList=this),t.hasAttribute("divider")&&!t.hasAttribute("role")&&t.setAttribute("role","separator");this.items_=i;const o=new Set;if(this.items_.forEach((t,e)=>{this.itemRoles?t.setAttribute("role",this.itemRoles):t.removeAttribute("role"),t.selected&&o.add(e)}),this.multi)this.select(o);else{const t=o.size?o.entries().next().value[1]:-1;this.select(t)}const s=new Event("items-updated",{bubbles:!0,composed:!0});this.dispatchEvent(s)}get selected(){const t=this.index;if(!te(t))return-1===t?null:this.items[t];const e=[];for(const i of t)e.push(this.items[i]);return e}get index(){return this.mdcFoundation?this.mdcFoundation.getSelectedIndex():-1}render(){const t=null===this.innerRole?void 0:this.innerRole,e=null===this.innerAriaLabel?void 0:this.innerAriaLabel,i=this.rootTabbable?"0":"-1";return r`
      <!-- @ts-ignore -->
      <ul
          tabindex=${i}
          role="${u(t)}"
          aria-label="${u(e)}"
          class="mdc-deprecated-list"
          @keydown=${this.onKeydown}
          @focusin=${this.onFocusIn}
          @focusout=${this.onFocusOut}
          @request-selected=${this.onRequestSelected}
          @list-item-rendered=${this.onListItemConnected}>
        <slot></slot>
        ${this.renderPlaceholder()}
      </ul>
    `}renderPlaceholder(){var t;const e=null!==(t=this.assignedElements)&&void 0!==t?t:[];return void 0!==this.emptyMessage&&0===e.length?r`
        <mwc-list-item noninteractive>${this.emptyMessage}</mwc-list-item>
      `:null}firstUpdated(){super.firstUpdated(),this.items.length||(this.mdcFoundation.setMulti(this.multi),this.layout())}onFocusIn(t){if(this.mdcFoundation&&this.mdcRoot){const e=this.getIndexOfTarget(t);this.mdcFoundation.handleFocusIn(t,e)}}onFocusOut(t){if(this.mdcFoundation&&this.mdcRoot){const e=this.getIndexOfTarget(t);this.mdcFoundation.handleFocusOut(t,e)}}onKeydown(t){if(this.mdcFoundation&&this.mdcRoot){const e=this.getIndexOfTarget(t),i=t.target,o=oe(i);this.mdcFoundation.handleKeydown(t,o,e)}}onRequestSelected(t){if(this.mdcFoundation){let e=this.getIndexOfTarget(t);if(-1===e&&(this.layout(),e=this.getIndexOfTarget(t),-1===e))return;if(this.items[e].disabled)return;const i=t.detail.selected,o=t.detail.source;this.mdcFoundation.handleSingleSelection(e,"interaction"===o,i),t.stopPropagation()}}getIndexOfTarget(t){const e=this.items,i=t.composedPath();for(const t of i){let i=-1;if(S(t)&&oe(t)&&(i=e.indexOf(t)),-1!==i)return i}return-1}createAdapter(){return this.mdcAdapter={getListItemCount:()=>this.mdcRoot?this.items.length:0,getFocusedElementIndex:this.getFocusedItemIndex,getAttributeForElementIndex:(t,e)=>{if(!this.mdcRoot)return"";const i=this.items[t];return i?i.getAttribute(e):""},setAttributeForElementIndex:(t,e,i)=>{if(!this.mdcRoot)return;const o=this.items[t];o&&o.setAttribute(e,i)},focusItemAtIndex:t=>{const e=this.items[t];e&&e.focus()},setTabIndexForElementIndex:(t,e)=>{const i=this.items[t];i&&(i.tabindex=e)},notifyAction:t=>{const e={bubbles:!0,composed:!0};e.detail={index:t};const i=new CustomEvent("action",e);this.dispatchEvent(i)},notifySelected:(t,e)=>{const i={bubbles:!0,composed:!0};i.detail={index:t,diff:e};const o=new CustomEvent("selected",i);this.dispatchEvent(o)},isFocusInsideList:()=>O(this),isRootFocused:()=>{const t=this.mdcRoot;return t.getRootNode().activeElement===t},setDisabledStateForElementIndex:(t,e)=>{const i=this.items[t];i&&(i.disabled=e)},getDisabledStateForElementIndex:t=>{const e=this.items[t];return!!e&&e.disabled},setSelectedStateForElementIndex:(t,e)=>{const i=this.items[t];i&&(i.selected=e)},getSelectedStateForElementIndex:t=>{const e=this.items[t];return!!e&&e.selected},setActivatedStateForElementIndex:(t,e)=>{const i=this.items[t];i&&(i.activated=e)}},this.mdcAdapter}selectUi(t,e=!1){const i=this.items[t];i&&(i.selected=!0,i.activated=e)}deselectUi(t){const e=this.items[t];e&&(e.selected=!1,e.activated=!1)}select(t){this.mdcFoundation&&this.mdcFoundation.setSelectedIndex(t)}toggle(t,e){this.multi&&this.mdcFoundation.toggleMultiAtIndex(t,e)}onListItemConnected(t){const e=t.target;this.layout(-1===this.items.indexOf(e))}layout(t=!0){t&&this.updateItems();const e=this.items[0];for(const t of this.items)t.tabindex=-1;e&&(this.noninteractive?this.previousTabindex||(this.previousTabindex=e):e.tabindex=0),this.itemsReadyResolver()}getFocusedItemIndex(){if(!this.mdcRoot)return-1;if(!this.items.length)return-1;const t=F();if(!t.length)return-1;for(let e=t.length-1;e>=0;e--){const i=t[e];if(oe(i))return this.items.indexOf(i)}return-1}focusItemAtIndex(t){for(const t of this.items)if(0===t.tabindex){t.tabindex=-1;break}this.items[t].tabindex=0,this.items[t].focus()}focus(){const t=this.mdcRoot;t&&t.focus()}blur(){const t=this.mdcRoot;t&&t.blur()}}t([i({type:String})],ae.prototype,"emptyMessage",void 0),t([R(".mdc-deprecated-list")],ae.prototype,"mdcRoot",void 0),t([Z("",!0,"*")],ae.prototype,"assignedElements",void 0),t([Z("",!0,'[tabindex="0"]')],ae.prototype,"tabbableElements",void 0),t([i({type:Boolean}),Q((function(t){this.mdcFoundation&&this.mdcFoundation.setUseActivatedClass(t)}))],ae.prototype,"activatable",void 0),t([i({type:Boolean}),Q((function(t,e){this.mdcFoundation&&this.mdcFoundation.setMulti(t),void 0!==e&&this.layout()}))],ae.prototype,"multi",void 0),t([i({type:Boolean}),Q((function(t){this.mdcFoundation&&this.mdcFoundation.setWrapFocus(t)}))],ae.prototype,"wrapFocus",void 0),t([i({type:String}),Q((function(t,e){void 0!==e&&this.updateItems()}))],ae.prototype,"itemRoles",void 0),t([i({type:String})],ae.prototype,"innerRole",void 0),t([i({type:String})],ae.prototype,"innerAriaLabel",void 0),t([i({type:Boolean})],ae.prototype,"rootTabbable",void 0),t([i({type:Boolean,reflect:!0}),Q((function(t){var e,i;if(t){const t=null!==(i=null===(e=this.tabbableElements)||void 0===e?void 0:e[0])&&void 0!==i?i:null;this.previousTabindex=t,t&&t.setAttribute("tabindex","-1")}else!t&&this.previousTabindex&&(this.previousTabindex.setAttribute("tabindex","0"),this.previousTabindex=null)}))],ae.prototype,"noninteractive",void 0);const ne=c`@keyframes mdc-ripple-fg-radius-in{from{animation-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transform:translate(var(--mdc-ripple-fg-translate-start, 0)) scale(1)}to{transform:translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))}}@keyframes mdc-ripple-fg-opacity-in{from{animation-timing-function:linear;opacity:0}to{opacity:var(--mdc-ripple-fg-opacity, 0)}}@keyframes mdc-ripple-fg-opacity-out{from{animation-timing-function:linear;opacity:var(--mdc-ripple-fg-opacity, 0)}to{opacity:0}}:host{display:block}.mdc-deprecated-list{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-subtitle1-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:1rem;font-size:var(--mdc-typography-subtitle1-font-size, 1rem);line-height:1.75rem;line-height:var(--mdc-typography-subtitle1-line-height, 1.75rem);font-weight:400;font-weight:var(--mdc-typography-subtitle1-font-weight, 400);letter-spacing:0.009375em;letter-spacing:var(--mdc-typography-subtitle1-letter-spacing, 0.009375em);text-decoration:inherit;text-decoration:var(--mdc-typography-subtitle1-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-subtitle1-text-transform, inherit);line-height:1.5rem;margin:0;padding:8px 0;list-style-type:none;color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));padding:var(--mdc-list-vertical-padding, 8px) 0}.mdc-deprecated-list:focus{outline:none}.mdc-deprecated-list-item{height:48px}.mdc-deprecated-list--dense{padding-top:4px;padding-bottom:4px;font-size:.812rem}.mdc-deprecated-list ::slotted([divider]){height:0;margin:0;border:none;border-bottom-width:1px;border-bottom-style:solid;border-bottom-color:rgba(0, 0, 0, 0.12)}.mdc-deprecated-list ::slotted([divider][padded]){margin:0 var(--mdc-list-side-padding, 16px)}.mdc-deprecated-list ::slotted([divider][inset]){margin-left:var(--mdc-list-inset-margin, 72px);margin-right:0;width:calc( 100% - var(--mdc-list-inset-margin, 72px) )}[dir=rtl] .mdc-deprecated-list ::slotted([divider][inset]),.mdc-deprecated-list ::slotted([divider][inset][dir=rtl]){margin-left:0;margin-right:var(--mdc-list-inset-margin, 72px)}.mdc-deprecated-list ::slotted([divider][inset][padded]){width:calc( 100% - var(--mdc-list-inset-margin, 72px) - var(--mdc-list-side-padding, 16px) )}.mdc-deprecated-list--dense ::slotted([mwc-list-item]){height:40px}.mdc-deprecated-list--dense ::slotted([mwc-list]){--mdc-list-item-graphic-size: 20px}.mdc-deprecated-list--two-line.mdc-deprecated-list--dense ::slotted([mwc-list-item]),.mdc-deprecated-list--avatar-list.mdc-deprecated-list--dense ::slotted([mwc-list-item]){height:60px}.mdc-deprecated-list--avatar-list.mdc-deprecated-list--dense ::slotted([mwc-list]){--mdc-list-item-graphic-size: 36px}:host([noninteractive]){pointer-events:none;cursor:default}.mdc-deprecated-list--dense ::slotted(.mdc-deprecated-list-item__primary-text){display:block;margin-top:0;line-height:normal;margin-bottom:-20px}.mdc-deprecated-list--dense ::slotted(.mdc-deprecated-list-item__primary-text)::before{display:inline-block;width:0;height:24px;content:"";vertical-align:0}.mdc-deprecated-list--dense ::slotted(.mdc-deprecated-list-item__primary-text)::after{display:inline-block;width:0;height:20px;content:"";vertical-align:-20px}`;let re=class extends ae{};re.styles=[ne],re=t([l("mwc-list")],re);var de,ce,le={ANCHOR:"mdc-menu-surface--anchor",ANIMATING_CLOSED:"mdc-menu-surface--animating-closed",ANIMATING_OPEN:"mdc-menu-surface--animating-open",FIXED:"mdc-menu-surface--fixed",IS_OPEN_BELOW:"mdc-menu-surface--is-open-below",OPEN:"mdc-menu-surface--open",ROOT:"mdc-menu-surface"},he={CLOSED_EVENT:"MDCMenuSurface:closed",CLOSING_EVENT:"MDCMenuSurface:closing",OPENED_EVENT:"MDCMenuSurface:opened",FOCUSABLE_ELEMENTS:["button:not(:disabled)",'[href]:not([aria-disabled="true"])',"input:not(:disabled)","select:not(:disabled)","textarea:not(:disabled)",'[tabindex]:not([tabindex="-1"]):not([aria-disabled="true"])'].join(", ")},pe={TRANSITION_OPEN_DURATION:120,TRANSITION_CLOSE_DURATION:75,MARGIN_TO_EDGE:32,ANCHOR_TO_MENU_SURFACE_WIDTH_RATIO:.67};!function(t){t[t.BOTTOM=1]="BOTTOM",t[t.CENTER=2]="CENTER",t[t.RIGHT=4]="RIGHT",t[t.FLIP_RTL=8]="FLIP_RTL"}(de||(de={})),function(t){t[t.TOP_LEFT=0]="TOP_LEFT",t[t.TOP_RIGHT=4]="TOP_RIGHT",t[t.BOTTOM_LEFT=1]="BOTTOM_LEFT",t[t.BOTTOM_RIGHT=5]="BOTTOM_RIGHT",t[t.TOP_START=8]="TOP_START",t[t.TOP_END=12]="TOP_END",t[t.BOTTOM_START=9]="BOTTOM_START",t[t.BOTTOM_END=13]="BOTTOM_END"}(ce||(ce={}));var me=function(t){function e(i){var o=t.call(this,z(z({},e.defaultAdapter),i))||this;return o.isSurfaceOpen=!1,o.isQuickOpen=!1,o.isHoistedElement=!1,o.isFixedPosition=!1,o.isHorizontallyCenteredOnViewport=!1,o.maxHeight=0,o.openAnimationEndTimerId=0,o.closeAnimationEndTimerId=0,o.animationRequestId=0,o.anchorCorner=ce.TOP_START,o.originCorner=ce.TOP_START,o.anchorMargin={top:0,right:0,bottom:0,left:0},o.position={x:0,y:0},o}return $(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return le},enumerable:!1,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return he},enumerable:!1,configurable:!0}),Object.defineProperty(e,"numbers",{get:function(){return pe},enumerable:!1,configurable:!0}),Object.defineProperty(e,"Corner",{get:function(){return ce},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},hasClass:function(){return!1},hasAnchor:function(){return!1},isElementInContainer:function(){return!1},isFocused:function(){return!1},isRtl:function(){return!1},getInnerDimensions:function(){return{height:0,width:0}},getAnchorDimensions:function(){return null},getWindowDimensions:function(){return{height:0,width:0}},getBodyDimensions:function(){return{height:0,width:0}},getWindowScroll:function(){return{x:0,y:0}},setPosition:function(){},setMaxHeight:function(){},setTransformOrigin:function(){},saveFocus:function(){},restoreFocus:function(){},notifyClose:function(){},notifyOpen:function(){},notifyClosing:function(){}}},enumerable:!1,configurable:!0}),e.prototype.init=function(){var t=e.cssClasses,i=t.ROOT,o=t.OPEN;if(!this.adapter.hasClass(i))throw new Error(i+" class required in root element.");this.adapter.hasClass(o)&&(this.isSurfaceOpen=!0)},e.prototype.destroy=function(){clearTimeout(this.openAnimationEndTimerId),clearTimeout(this.closeAnimationEndTimerId),cancelAnimationFrame(this.animationRequestId)},e.prototype.setAnchorCorner=function(t){this.anchorCorner=t},e.prototype.flipCornerHorizontally=function(){this.originCorner=this.originCorner^de.RIGHT},e.prototype.setAnchorMargin=function(t){this.anchorMargin.top=t.top||0,this.anchorMargin.right=t.right||0,this.anchorMargin.bottom=t.bottom||0,this.anchorMargin.left=t.left||0},e.prototype.setIsHoisted=function(t){this.isHoistedElement=t},e.prototype.setFixedPosition=function(t){this.isFixedPosition=t},e.prototype.setAbsolutePosition=function(t,e){this.position.x=this.isFinite(t)?t:0,this.position.y=this.isFinite(e)?e:0},e.prototype.setIsHorizontallyCenteredOnViewport=function(t){this.isHorizontallyCenteredOnViewport=t},e.prototype.setQuickOpen=function(t){this.isQuickOpen=t},e.prototype.setMaxHeight=function(t){this.maxHeight=t},e.prototype.isOpen=function(){return this.isSurfaceOpen},e.prototype.open=function(){var t=this;this.isSurfaceOpen||(this.adapter.saveFocus(),this.isQuickOpen?(this.isSurfaceOpen=!0,this.adapter.addClass(e.cssClasses.OPEN),this.dimensions=this.adapter.getInnerDimensions(),this.autoposition(),this.adapter.notifyOpen()):(this.adapter.addClass(e.cssClasses.ANIMATING_OPEN),this.animationRequestId=requestAnimationFrame((function(){t.dimensions=t.adapter.getInnerDimensions(),t.autoposition(),t.adapter.addClass(e.cssClasses.OPEN),t.openAnimationEndTimerId=setTimeout((function(){t.openAnimationEndTimerId=0,t.adapter.removeClass(e.cssClasses.ANIMATING_OPEN),t.adapter.notifyOpen()}),pe.TRANSITION_OPEN_DURATION)})),this.isSurfaceOpen=!0))},e.prototype.close=function(t){var i=this;if(void 0===t&&(t=!1),this.isSurfaceOpen){if(this.adapter.notifyClosing(),this.isQuickOpen)return this.isSurfaceOpen=!1,t||this.maybeRestoreFocus(),this.adapter.removeClass(e.cssClasses.OPEN),this.adapter.removeClass(e.cssClasses.IS_OPEN_BELOW),void this.adapter.notifyClose();this.adapter.addClass(e.cssClasses.ANIMATING_CLOSED),requestAnimationFrame((function(){i.adapter.removeClass(e.cssClasses.OPEN),i.adapter.removeClass(e.cssClasses.IS_OPEN_BELOW),i.closeAnimationEndTimerId=setTimeout((function(){i.closeAnimationEndTimerId=0,i.adapter.removeClass(e.cssClasses.ANIMATING_CLOSED),i.adapter.notifyClose()}),pe.TRANSITION_CLOSE_DURATION)})),this.isSurfaceOpen=!1,t||this.maybeRestoreFocus()}},e.prototype.handleBodyClick=function(t){var e=t.target;this.adapter.isElementInContainer(e)||this.close()},e.prototype.handleKeydown=function(t){var e=t.keyCode;("Escape"===t.key||27===e)&&this.close()},e.prototype.autoposition=function(){var t;this.measurements=this.getAutoLayoutmeasurements();var i=this.getoriginCorner(),o=this.getMenuSurfaceMaxHeight(i),s=this.hasBit(i,de.BOTTOM)?"bottom":"top",a=this.hasBit(i,de.RIGHT)?"right":"left",n=this.getHorizontalOriginOffset(i),r=this.getVerticalOriginOffset(i),d=this.measurements,c=d.anchorSize,l=d.surfaceSize,h=((t={})[a]=n,t[s]=r,t);c.width/l.width>pe.ANCHOR_TO_MENU_SURFACE_WIDTH_RATIO&&(a="center"),(this.isHoistedElement||this.isFixedPosition)&&this.adjustPositionForHoistedElement(h),this.adapter.setTransformOrigin(a+" "+s),this.adapter.setPosition(h),this.adapter.setMaxHeight(o?o+"px":""),this.hasBit(i,de.BOTTOM)||this.adapter.addClass(e.cssClasses.IS_OPEN_BELOW)},e.prototype.getAutoLayoutmeasurements=function(){var t=this.adapter.getAnchorDimensions(),e=this.adapter.getBodyDimensions(),i=this.adapter.getWindowDimensions(),o=this.adapter.getWindowScroll();return t||(t={top:this.position.y,right:this.position.x,bottom:this.position.y,left:this.position.x,width:0,height:0}),{anchorSize:t,bodySize:e,surfaceSize:this.dimensions,viewportDistance:{top:t.top,right:i.width-t.right,bottom:i.height-t.bottom,left:t.left},viewportSize:i,windowScroll:o}},e.prototype.getoriginCorner=function(){var t,i,o=this.originCorner,s=this.measurements,a=s.viewportDistance,n=s.anchorSize,r=s.surfaceSize,d=e.numbers.MARGIN_TO_EDGE;this.hasBit(this.anchorCorner,de.BOTTOM)?(t=a.top-d+this.anchorMargin.bottom,i=a.bottom-d-this.anchorMargin.bottom):(t=a.top-d+this.anchorMargin.top,i=a.bottom-d+n.height-this.anchorMargin.top),!(i-r.height>0)&&t>i&&(o=this.setBit(o,de.BOTTOM));var c,l,h=this.adapter.isRtl(),p=this.hasBit(this.anchorCorner,de.FLIP_RTL),m=this.hasBit(this.anchorCorner,de.RIGHT)||this.hasBit(o,de.RIGHT),u=!1;(u=h&&p?!m:m)?(c=a.left+n.width+this.anchorMargin.right,l=a.right-this.anchorMargin.right):(c=a.left+this.anchorMargin.left,l=a.right+n.width-this.anchorMargin.left);var f=c-r.width>0,g=l-r.width>0,b=this.hasBit(o,de.FLIP_RTL)&&this.hasBit(o,de.RIGHT);return g&&b&&h||!f&&b?o=this.unsetBit(o,de.RIGHT):(f&&u&&h||f&&!u&&m||!g&&c>=l)&&(o=this.setBit(o,de.RIGHT)),o},e.prototype.getMenuSurfaceMaxHeight=function(t){if(this.maxHeight>0)return this.maxHeight;var i=this.measurements.viewportDistance,o=0,s=this.hasBit(t,de.BOTTOM),a=this.hasBit(this.anchorCorner,de.BOTTOM),n=e.numbers.MARGIN_TO_EDGE;return s?(o=i.top+this.anchorMargin.top-n,a||(o+=this.measurements.anchorSize.height)):(o=i.bottom-this.anchorMargin.bottom+this.measurements.anchorSize.height-n,a&&(o-=this.measurements.anchorSize.height)),o},e.prototype.getHorizontalOriginOffset=function(t){var e=this.measurements.anchorSize,i=this.hasBit(t,de.RIGHT),o=this.hasBit(this.anchorCorner,de.RIGHT);if(i){var s=o?e.width-this.anchorMargin.left:this.anchorMargin.right;return this.isHoistedElement||this.isFixedPosition?s-(this.measurements.viewportSize.width-this.measurements.bodySize.width):s}return o?e.width-this.anchorMargin.right:this.anchorMargin.left},e.prototype.getVerticalOriginOffset=function(t){var e=this.measurements.anchorSize,i=this.hasBit(t,de.BOTTOM),o=this.hasBit(this.anchorCorner,de.BOTTOM);return i?o?e.height-this.anchorMargin.top:-this.anchorMargin.bottom:o?e.height+this.anchorMargin.bottom:this.anchorMargin.top},e.prototype.adjustPositionForHoistedElement=function(t){var e,i,o=this.measurements,s=o.windowScroll,a=o.viewportDistance,n=o.surfaceSize,r=o.viewportSize,d=Object.keys(t);try{for(var c=L(d),l=c.next();!l.done;l=c.next()){var h=l.value,p=t[h]||0;!this.isHorizontallyCenteredOnViewport||"left"!==h&&"right"!==h?(p+=a[h],this.isFixedPosition||("top"===h?p+=s.y:"bottom"===h?p-=s.y:"left"===h?p+=s.x:p-=s.x),t[h]=p):t[h]=(r.width-n.width)/2}}catch(t){e={error:t}}finally{try{l&&!l.done&&(i=c.return)&&i.call(c)}finally{if(e)throw e.error}}},e.prototype.maybeRestoreFocus=function(){var t=this.adapter.isFocused(),e=document.activeElement&&this.adapter.isElementInContainer(document.activeElement);(t||e)&&this.adapter.restoreFocus()},e.prototype.hasBit=function(t,e){return Boolean(t&e)},e.prototype.setBit=function(t,e){return t|e},e.prototype.unsetBit=function(t,e){return t^e},e.prototype.isFinite=function(t){return"number"==typeof t&&isFinite(t)},e}(A),ue=me;const fe={TOP_LEFT:ce.TOP_LEFT,TOP_RIGHT:ce.TOP_RIGHT,BOTTOM_LEFT:ce.BOTTOM_LEFT,BOTTOM_RIGHT:ce.BOTTOM_RIGHT,TOP_START:ce.TOP_START,TOP_END:ce.TOP_END,BOTTOM_START:ce.BOTTOM_START,BOTTOM_END:ce.BOTTOM_END};class ge extends C{constructor(){super(...arguments),this.mdcFoundationClass=ue,this.absolute=!1,this.fullwidth=!1,this.fixed=!1,this.x=null,this.y=null,this.quick=!1,this.open=!1,this.stayOpenOnBodyClick=!1,this.bitwiseCorner=ce.TOP_START,this.previousMenuCorner=null,this.menuCorner="START",this.corner="TOP_START",this.styleTop="",this.styleLeft="",this.styleRight="",this.styleBottom="",this.styleMaxHeight="",this.styleTransformOrigin="",this.anchor=null,this.previouslyFocused=null,this.previousAnchor=null,this.onBodyClickBound=()=>{}}render(){const t={"mdc-menu-surface--fixed":this.fixed,"mdc-menu-surface--fullwidth":this.fullwidth},e={top:this.styleTop,left:this.styleLeft,right:this.styleRight,bottom:this.styleBottom,"max-height":this.styleMaxHeight,"transform-origin":this.styleTransformOrigin};return r`
      <div
          class="mdc-menu-surface ${d(t)}"
          style="${M(e)}"
          @keydown=${this.onKeydown}
          @opened=${this.registerBodyClick}
          @closed=${this.deregisterBodyClick}>
        <slot></slot>
      </div>`}createAdapter(){return Object.assign(Object.assign({},B(this.mdcRoot)),{hasAnchor:()=>!!this.anchor,notifyClose:()=>{const t=new CustomEvent("closed",{bubbles:!0,composed:!0});this.open=!1,this.mdcRoot.dispatchEvent(t)},notifyClosing:()=>{const t=new CustomEvent("closing",{bubbles:!0,composed:!0});this.mdcRoot.dispatchEvent(t)},notifyOpen:()=>{const t=new CustomEvent("opened",{bubbles:!0,composed:!0});this.open=!0,this.mdcRoot.dispatchEvent(t)},isElementInContainer:()=>!1,isRtl:()=>!!this.mdcRoot&&"rtl"===getComputedStyle(this.mdcRoot).direction,setTransformOrigin:t=>{this.mdcRoot&&(this.styleTransformOrigin=t)},isFocused:()=>O(this),saveFocus:()=>{const t=F(),e=t.length;e||(this.previouslyFocused=null),this.previouslyFocused=t[e-1]},restoreFocus:()=>{this.previouslyFocused&&"focus"in this.previouslyFocused&&this.previouslyFocused.focus()},getInnerDimensions:()=>{const t=this.mdcRoot;return t?{width:t.offsetWidth,height:t.offsetHeight}:{width:0,height:0}},getAnchorDimensions:()=>{const t=this.anchor;return t?t.getBoundingClientRect():null},getBodyDimensions:()=>({width:document.body.clientWidth,height:document.body.clientHeight}),getWindowDimensions:()=>({width:window.innerWidth,height:window.innerHeight}),getWindowScroll:()=>({x:window.pageXOffset,y:window.pageYOffset}),setPosition:t=>{this.mdcRoot&&(this.styleLeft="left"in t?t.left+"px":"",this.styleRight="right"in t?t.right+"px":"",this.styleTop="top"in t?t.top+"px":"",this.styleBottom="bottom"in t?t.bottom+"px":"")},setMaxHeight:async t=>{this.mdcRoot&&(this.styleMaxHeight=t,await this.updateComplete,this.styleMaxHeight=`var(--mdc-menu-max-height, ${t})`)}})}onKeydown(t){this.mdcFoundation&&this.mdcFoundation.handleKeydown(t)}onBodyClick(t){if(this.stayOpenOnBodyClick)return;-1===t.composedPath().indexOf(this)&&this.close()}registerBodyClick(){this.onBodyClickBound=this.onBodyClick.bind(this),document.body.addEventListener("click",this.onBodyClickBound,{passive:!0,capture:!0})}deregisterBodyClick(){document.body.removeEventListener("click",this.onBodyClickBound,{capture:!0})}close(){this.open=!1}show(){this.open=!0}}t([R(".mdc-menu-surface")],ge.prototype,"mdcRoot",void 0),t([R("slot")],ge.prototype,"slotElement",void 0),t([i({type:Boolean}),Q((function(t){this.mdcFoundation&&!this.fixed&&this.mdcFoundation.setIsHoisted(t)}))],ge.prototype,"absolute",void 0),t([i({type:Boolean})],ge.prototype,"fullwidth",void 0),t([i({type:Boolean}),Q((function(t){this.mdcFoundation&&!this.absolute&&this.mdcFoundation.setFixedPosition(t)}))],ge.prototype,"fixed",void 0),t([i({type:Number}),Q((function(t){this.mdcFoundation&&null!==this.y&&null!==t&&(this.mdcFoundation.setAbsolutePosition(t,this.y),this.mdcFoundation.setAnchorMargin({left:t,top:this.y,right:-t,bottom:this.y}))}))],ge.prototype,"x",void 0),t([i({type:Number}),Q((function(t){this.mdcFoundation&&null!==this.x&&null!==t&&(this.mdcFoundation.setAbsolutePosition(this.x,t),this.mdcFoundation.setAnchorMargin({left:this.x,top:t,right:-this.x,bottom:t}))}))],ge.prototype,"y",void 0),t([i({type:Boolean}),Q((function(t){this.mdcFoundation&&this.mdcFoundation.setQuickOpen(t)}))],ge.prototype,"quick",void 0),t([i({type:Boolean,reflect:!0}),Q((function(t,e){this.mdcFoundation&&(t?this.mdcFoundation.open():void 0!==e&&this.mdcFoundation.close())}))],ge.prototype,"open",void 0),t([i({type:Boolean})],ge.prototype,"stayOpenOnBodyClick",void 0),t([o(),Q((function(t){this.mdcFoundation&&this.mdcFoundation.setAnchorCorner(t)}))],ge.prototype,"bitwiseCorner",void 0),t([i({type:String}),Q((function(t){if(this.mdcFoundation){const e="START"===t||"END"===t,i=null===this.previousMenuCorner,o=!i&&t!==this.previousMenuCorner,s=i&&"END"===t;e&&(o||s)&&(this.bitwiseCorner=this.bitwiseCorner^de.RIGHT,this.mdcFoundation.flipCornerHorizontally(),this.previousMenuCorner=t)}}))],ge.prototype,"menuCorner",void 0),t([i({type:String}),Q((function(t){if(this.mdcFoundation&&t){let e=fe[t];"END"===this.menuCorner&&(e^=de.RIGHT),this.bitwiseCorner=e}}))],ge.prototype,"corner",void 0),t([o()],ge.prototype,"styleTop",void 0),t([o()],ge.prototype,"styleLeft",void 0),t([o()],ge.prototype,"styleRight",void 0),t([o()],ge.prototype,"styleBottom",void 0),t([o()],ge.prototype,"styleMaxHeight",void 0),t([o()],ge.prototype,"styleTransformOrigin",void 0);const be=c`.mdc-menu-surface{display:none;position:absolute;box-sizing:border-box;max-width:calc(100vw - 32px);max-width:var(--mdc-menu-max-width, calc(100vw - 32px));max-height:calc(100vh - 32px);max-height:var(--mdc-menu-max-height, calc(100vh - 32px));margin:0;padding:0;transform:scale(1);transform-origin:top left;opacity:0;overflow:auto;will-change:transform,opacity;z-index:8;transition:opacity .03s linear,transform .12s cubic-bezier(0, 0, 0.2, 1),height 250ms cubic-bezier(0, 0, 0.2, 1);box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12);background-color:#fff;background-color:var(--mdc-theme-surface, #fff);color:#000;color:var(--mdc-theme-on-surface, #000);border-radius:4px;border-radius:var(--mdc-shape-medium, 4px);transform-origin-left:top left;transform-origin-right:top right}.mdc-menu-surface:focus{outline:none}.mdc-menu-surface--animating-open{display:inline-block;transform:scale(0.8);opacity:0}.mdc-menu-surface--open{display:inline-block;transform:scale(1);opacity:1}.mdc-menu-surface--animating-closed{display:inline-block;opacity:0;transition:opacity .075s linear}[dir=rtl] .mdc-menu-surface,.mdc-menu-surface[dir=rtl]{transform-origin-left:top right;transform-origin-right:top left}.mdc-menu-surface--anchor{position:relative;overflow:visible}.mdc-menu-surface--fixed{position:fixed}.mdc-menu-surface--fullwidth{width:100%}:host(:not([open])){display:none}.mdc-menu-surface{z-index:8;z-index:var(--mdc-menu-z-index, 8);min-width:112px;min-width:var(--mdc-menu-min-width, 112px)}`;let xe=class extends ge{};xe.styles=[be],xe=t([l("mwc-menu-surface")],xe);var ve,ye={MENU_SELECTED_LIST_ITEM:"mdc-menu-item--selected",MENU_SELECTION_GROUP:"mdc-menu__selection-group",ROOT:"mdc-menu"},_e={ARIA_CHECKED_ATTR:"aria-checked",ARIA_DISABLED_ATTR:"aria-disabled",CHECKBOX_SELECTOR:'input[type="checkbox"]',LIST_SELECTOR:".mdc-list,.mdc-deprecated-list",SELECTED_EVENT:"MDCMenu:selected"},we={FOCUS_ROOT_INDEX:-1};!function(t){t[t.NONE=0]="NONE",t[t.LIST_ROOT=1]="LIST_ROOT",t[t.FIRST_ITEM=2]="FIRST_ITEM",t[t.LAST_ITEM=3]="LAST_ITEM"}(ve||(ve={}));var Ie=function(t){function e(i){var o=t.call(this,z(z({},e.defaultAdapter),i))||this;return o.closeAnimationEndTimerId=0,o.defaultFocusState=ve.LIST_ROOT,o.selectedIndex=-1,o}return $(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return ye},enumerable:!1,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return _e},enumerable:!1,configurable:!0}),Object.defineProperty(e,"numbers",{get:function(){return we},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClassToElementAtIndex:function(){},removeClassFromElementAtIndex:function(){},addAttributeToElementAtIndex:function(){},removeAttributeFromElementAtIndex:function(){},elementContainsClass:function(){return!1},closeSurface:function(){},getElementIndex:function(){return-1},notifySelected:function(){},getMenuItemCount:function(){return 0},focusItemAtIndex:function(){},focusListRoot:function(){},getSelectedSiblingOfItemAtIndex:function(){return-1},isSelectableItemAtIndex:function(){return!1}}},enumerable:!1,configurable:!0}),e.prototype.destroy=function(){this.closeAnimationEndTimerId&&clearTimeout(this.closeAnimationEndTimerId),this.adapter.closeSurface()},e.prototype.handleKeydown=function(t){var e=t.key,i=t.keyCode;("Tab"===e||9===i)&&this.adapter.closeSurface(!0)},e.prototype.handleItemAction=function(t){var e=this,i=this.adapter.getElementIndex(t);i<0||(this.adapter.notifySelected({index:i}),this.adapter.closeSurface(),this.closeAnimationEndTimerId=setTimeout((function(){var i=e.adapter.getElementIndex(t);i>=0&&e.adapter.isSelectableItemAtIndex(i)&&e.setSelectedIndex(i)}),me.numbers.TRANSITION_CLOSE_DURATION))},e.prototype.handleMenuSurfaceOpened=function(){switch(this.defaultFocusState){case ve.FIRST_ITEM:this.adapter.focusItemAtIndex(0);break;case ve.LAST_ITEM:this.adapter.focusItemAtIndex(this.adapter.getMenuItemCount()-1);break;case ve.NONE:break;default:this.adapter.focusListRoot()}},e.prototype.setDefaultFocusState=function(t){this.defaultFocusState=t},e.prototype.getSelectedIndex=function(){return this.selectedIndex},e.prototype.setSelectedIndex=function(t){if(this.validatedIndex(t),!this.adapter.isSelectableItemAtIndex(t))throw new Error("MDCMenuFoundation: No selection group at specified index.");var e=this.adapter.getSelectedSiblingOfItemAtIndex(t);e>=0&&(this.adapter.removeAttributeFromElementAtIndex(e,_e.ARIA_CHECKED_ATTR),this.adapter.removeClassFromElementAtIndex(e,ye.MENU_SELECTED_LIST_ITEM)),this.adapter.addClassToElementAtIndex(t,ye.MENU_SELECTED_LIST_ITEM),this.adapter.addAttributeToElementAtIndex(t,_e.ARIA_CHECKED_ATTR,"true"),this.selectedIndex=t},e.prototype.setEnabled=function(t,e){this.validatedIndex(t),e?(this.adapter.removeClassFromElementAtIndex(t,Gt),this.adapter.addAttributeToElementAtIndex(t,_e.ARIA_DISABLED_ATTR,"false")):(this.adapter.addClassToElementAtIndex(t,Gt),this.adapter.addAttributeToElementAtIndex(t,_e.ARIA_DISABLED_ATTR,"true"))},e.prototype.validatedIndex=function(t){var e=this.adapter.getMenuItemCount();if(!(t>=0&&t<e))throw new Error("MDCMenuFoundation: No list item at specified index.")},e}(A);class Ee extends C{constructor(){super(...arguments),this.mdcFoundationClass=Ie,this.listElement_=null,this.anchor=null,this.open=!1,this.quick=!1,this.wrapFocus=!1,this.innerRole="menu",this.corner="TOP_START",this.x=null,this.y=null,this.absolute=!1,this.multi=!1,this.activatable=!1,this.fixed=!1,this.forceGroupSelection=!1,this.fullwidth=!1,this.menuCorner="START",this.stayOpenOnBodyClick=!1,this.defaultFocus="LIST_ROOT",this._listUpdateComplete=null}get listElement(){return this.listElement_||(this.listElement_=this.renderRoot.querySelector("mwc-list")),this.listElement_}get items(){const t=this.listElement;return t?t.items:[]}get index(){const t=this.listElement;return t?t.index:-1}get selected(){const t=this.listElement;return t?t.selected:null}render(){const t="menu"===this.innerRole?"menuitem":"option";return r`
      <mwc-menu-surface
          ?hidden=${!this.open}
          .anchor=${this.anchor}
          .open=${this.open}
          .quick=${this.quick}
          .corner=${this.corner}
          .x=${this.x}
          .y=${this.y}
          .absolute=${this.absolute}
          .fixed=${this.fixed}
          .fullwidth=${this.fullwidth}
          .menuCorner=${this.menuCorner}
          ?stayOpenOnBodyClick=${this.stayOpenOnBodyClick}
          class="mdc-menu mdc-menu-surface"
          @closed=${this.onClosed}
          @opened=${this.onOpened}
          @keydown=${this.onKeydown}>
        <mwc-list
          rootTabbable
          .innerRole=${this.innerRole}
          .multi=${this.multi}
          class="mdc-deprecated-list"
          .itemRoles=${t}
          .wrapFocus=${this.wrapFocus}
          .activatable=${this.activatable}
          @action=${this.onAction}>
        <slot></slot>
      </mwc-list>
    </mwc-menu-surface>`}createAdapter(){return{addClassToElementAtIndex:(t,e)=>{const i=this.listElement;if(!i)return;const o=i.items[t];o&&("mdc-menu-item--selected"===e?this.forceGroupSelection&&!o.selected&&i.toggle(t,!0):o.classList.add(e))},removeClassFromElementAtIndex:(t,e)=>{const i=this.listElement;if(!i)return;const o=i.items[t];o&&("mdc-menu-item--selected"===e?o.selected&&i.toggle(t,!1):o.classList.remove(e))},addAttributeToElementAtIndex:(t,e,i)=>{const o=this.listElement;if(!o)return;const s=o.items[t];s&&s.setAttribute(e,i)},removeAttributeFromElementAtIndex:(t,e)=>{const i=this.listElement;if(!i)return;const o=i.items[t];o&&o.removeAttribute(e)},elementContainsClass:(t,e)=>t.classList.contains(e),closeSurface:()=>{this.open=!1},getElementIndex:t=>{const e=this.listElement;return e?e.items.indexOf(t):-1},notifySelected:()=>{},getMenuItemCount:()=>{const t=this.listElement;return t?t.items.length:0},focusItemAtIndex:t=>{const e=this.listElement;if(!e)return;const i=e.items[t];i&&i.focus()},focusListRoot:()=>{this.listElement&&this.listElement.focus()},getSelectedSiblingOfItemAtIndex:t=>{const e=this.listElement;if(!e)return-1;const i=e.items[t];if(!i||!i.group)return-1;for(let o=0;o<e.items.length;o++){if(o===t)continue;const s=e.items[o];if(s.selected&&s.group===i.group)return o}return-1},isSelectableItemAtIndex:t=>{const e=this.listElement;if(!e)return!1;const i=e.items[t];return!!i&&i.hasAttribute("group")}}}onKeydown(t){this.mdcFoundation&&this.mdcFoundation.handleKeydown(t)}onAction(t){const e=this.listElement;if(this.mdcFoundation&&e){const i=t.detail.index,o=e.items[i];o&&this.mdcFoundation.handleItemAction(o)}}onOpened(){this.open=!0,this.mdcFoundation&&this.mdcFoundation.handleMenuSurfaceOpened()}onClosed(){this.open=!1}async getUpdateComplete(){await this._listUpdateComplete;return await super.getUpdateComplete()}async firstUpdated(){super.firstUpdated();const t=this.listElement;t&&(this._listUpdateComplete=t.updateComplete,await this._listUpdateComplete)}select(t){const e=this.listElement;e&&e.select(t)}close(){this.open=!1}show(){this.open=!0}getFocusedItemIndex(){const t=this.listElement;return t?t.getFocusedItemIndex():-1}focusItemAtIndex(t){const e=this.listElement;e&&e.focusItemAtIndex(t)}layout(t=!0){const e=this.listElement;e&&e.layout(t)}}t([R(".mdc-menu")],Ee.prototype,"mdcRoot",void 0),t([R("slot")],Ee.prototype,"slotElement",void 0),t([i({type:Object})],Ee.prototype,"anchor",void 0),t([i({type:Boolean,reflect:!0})],Ee.prototype,"open",void 0),t([i({type:Boolean})],Ee.prototype,"quick",void 0),t([i({type:Boolean})],Ee.prototype,"wrapFocus",void 0),t([i({type:String})],Ee.prototype,"innerRole",void 0),t([i({type:String})],Ee.prototype,"corner",void 0),t([i({type:Number})],Ee.prototype,"x",void 0),t([i({type:Number})],Ee.prototype,"y",void 0),t([i({type:Boolean})],Ee.prototype,"absolute",void 0),t([i({type:Boolean})],Ee.prototype,"multi",void 0),t([i({type:Boolean})],Ee.prototype,"activatable",void 0),t([i({type:Boolean})],Ee.prototype,"fixed",void 0),t([i({type:Boolean})],Ee.prototype,"forceGroupSelection",void 0),t([i({type:Boolean})],Ee.prototype,"fullwidth",void 0),t([i({type:String})],Ee.prototype,"menuCorner",void 0),t([i({type:Boolean})],Ee.prototype,"stayOpenOnBodyClick",void 0),t([i({type:String}),Q((function(t){this.mdcFoundation&&this.mdcFoundation.setDefaultFocusState(ve[t])}))],Ee.prototype,"defaultFocus",void 0);const ke=c`mwc-list ::slotted([mwc-list-item]:not([twoline])){height:var(--mdc-menu-item-height, 48px)}`;let Te=class extends Ee{};Te.styles=[ke],Te=t([l("mwc-menu")],Te),h([l("ha-button-menu")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[i()],key:"corner",value:()=>"TOP_START"},{kind:"field",decorators:[i({type:Boolean})],key:"multi",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"activatable",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"fixed",value:()=>!1},{kind:"field",decorators:[R("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var t;return null===(t=this._menu)||void 0===t?void 0:t.items}},{kind:"get",key:"selected",value:function(){var t;return null===(t=this._menu)||void 0===t?void 0:t.selected}},{kind:"method",key:"render",value:function(){return r`
      <div @click=${this._handleClick}>
        <slot name="trigger"></slot>
      </div>
      <mwc-menu
        .corner=${this.corner}
        .fixed=${this.fixed}
        .multi=${this.multi}
        .activatable=${this.activatable}
      >
        <slot></slot>
      </mwc-menu>
    `}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this,this._menu.show())}},{kind:"get",static:!0,key:"styles",value:function(){return c`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
    `}}]}}),a),h([l("hacs-tabbed-menu")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"configuration",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"hacs",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"narrow",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"repositories",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"lovelace",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"status",value:void 0},{kind:"method",key:"render",value:function(){var t,e,i;return r`
      <ha-button-menu corner="BOTTOM_START" slot="toolbar-icon">
        <mwc-icon-button slot="trigger" alt="menu">
          <ha-svg-icon .path=${x}></ha-svg-icon>
        </mwc-icon-button>

        <mwc-list-item action="documentation">
          <hacs-link url="https://hacs.xyz/">
            ${this.hacs.localize("menu.documentation")}
          </hacs-link>
        </mwc-list-item>

        ${0!==(null===(t=this.repositories)||void 0===t?void 0:t.filter(t=>t.new).length)?r`<mwc-list-item @click=${this._clearAllNewRepositories}>
              ${this.hacs.localize("menu.dismiss")}
            </mwc-list-item>`:""}

        <mwc-list-item><hacs-link url="https://github.com/hacs">GitHub</hacs-link></mwc-list-item>
        <mwc-list-item>
          <hacs-link url="https://hacs.xyz/docs/issues"
            >${this.hacs.localize("menu.open_issue")}</hacs-link
          >
        </mwc-list-item>

        ${null!==(e=this.status)&&void 0!==e&&e.disabled||null!==(i=this.status)&&void 0!==i&&i.background_task?"":r`<mwc-list-item @click=${this._showCustomRepositoriesDialog}>
              ${this.hacs.localize("menu.custom_repositories")}
            </mwc-list-item>`}

        <mwc-list-item @click=${this._showAboutDialog}>
          ${this.hacs.localize("menu.about")}
        </mwc-list-item>
      </ha-button-menu>
    `}},{kind:"method",key:"_clearAllNewRepositories",value:async function(){var t;await N(this.hass,(null===(t=D(this.hacs.language,this.route))||void 0===t?void 0:t.categories)||[])}},{kind:"method",key:"_showAboutDialog",value:function(){X(this,this.hacs)}},{kind:"method",key:"_showCustomRepositoriesDialog",value:function(){this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"custom-repositories",repositories:this.repositories},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return c``}}]}}),a);let Re=h([l("hacs-store-panel")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"filters",value:()=>({})},{kind:"field",decorators:[i({attribute:!1})],key:"hacs",value:void 0},{kind:"field",decorators:[i()],key:"_searchInput",value:()=>""},{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"narrow",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"isWide",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"repositories",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"sections",value:void 0},{kind:"field",decorators:[i()],key:"section",value:void 0},{kind:"field",key:"_repositoriesInActiveSection",value(){return f((t,e)=>[(null==t?void 0:t.filter(t=>{var i,o,s;return(null===(i=this.hacs.sections)||void 0===i||null===(o=i.find(t=>t.id===e))||void 0===o||null===(s=o.categories)||void 0===s?void 0:s.includes(t.category))&&t.installed}))||[],(null==t?void 0:t.filter(t=>{var i,o,s;return(null===(i=this.hacs.sections)||void 0===i||null===(o=i.find(t=>t.id===e))||void 0===o||null===(s=o.categories)||void 0===s?void 0:s.includes(t.category))&&t.new&&!t.installed}))||[]])}},{kind:"get",key:"allRepositories",value:function(){const[t,e]=this._repositoriesInActiveSection(this.repositories,this.section);return e.concat(t)}},{kind:"field",key:"_filterRepositories",value:()=>f(K)},{kind:"get",key:"visibleRepositories",value:function(){const t=this.allRepositories.filter(t=>{var e,i;return null===(e=this.filters[this.section])||void 0===e||null===(i=e.find(e=>e.id===t.category))||void 0===i?void 0:i.checked});return this._filterRepositories(t,this._searchInput)}},{kind:"method",key:"firstUpdated",value:async function(){this.addEventListener("filter-change",t=>this._updateFilters(t))}},{kind:"method",key:"_updateFilters",value:function(t){var e;const i=null===(e=this.filters[this.section])||void 0===e?void 0:e.find(e=>e.id===t.detail.id);this.filters[this.section].find(t=>t.id===i.id).checked=!i.checked,this.requestUpdate()}},{kind:"method",key:"render",value:function(){var t;if(!this.hacs)return r``;const e=this._repositoriesInActiveSection(this.repositories,this.section)[1];if(!this.filters[this.section]&&this.hacs.configuration.categories){var i;const t=null===(i=D(this.hacs.language,this.route))||void 0===i?void 0:i.categories;this.filters[this.section]=[],null==t||t.filter(t=>{var e;return null===(e=this.hacs.configuration)||void 0===e?void 0:e.categories.includes(t)}).forEach(t=>{this.filters[this.section].push({id:t,value:t,checked:!0})})}return r`<hass-tabs-subpage
      back-path="/hacs/entry"
      .hass=${this.hass}
      .narrow=${this.narrow}
      .route=${this.route}
      .tabs=${this.hacs.sections}
      hasFab
    >
      <hacs-tabbed-menu
        slot="toolbar-icon"
        .hass=${this.hass}
        .hacs=${this.hacs}
        .route=${this.route}
        .narrow=${this.narrow}
        .configuration=${this.hacs.configuration}
        .lovelace=${this.hacs.resources}
        .status=${this.hacs.status}
        .repositories=${this.repositories}
      >
      </hacs-tabbed-menu>
      ${this.narrow?r`
            <div slot="header">
              <slot name="header">
                <search-input
                  class="header"
                  no-label-float
                  .label=${this.hacs.localize("search.installed")}
                  .filter=${this._searchInput||""}
                  @value-changed=${this._inputValueChanged}
                ></search-input>
              </slot>
            </div>
          `:r`<div class="search">
            <search-input
              no-label-float
              .label=${0===e.length?this.hacs.localize("search.installed"):this.hacs.localize("search.installed_new")}
              .filter=${this._searchInput||""}
              @value-changed=${this._inputValueChanged}
            ></search-input>
          </div>`}
      <div class="content ${this.narrow?"narrow-content":""}">
        ${(null===(t=this.filters[this.section])||void 0===t?void 0:t.length)>1?r`<div class="filters">
              <hacs-filter
                .hacs=${this.hacs}
                .filters="${this.filters[this.section]}"
              ></hacs-filter>
            </div>`:""}
        ${(null==e?void 0:e.length)>10?r`<div class="new-repositories">
              ${this.hacs.localize("store.new_repositories_note")}
            </div>`:""}
        <div class="container ${this.narrow?"narrow":""}">
          ${void 0===this.repositories?"":0===this.allRepositories.length?this._renderEmpty():0===this.visibleRepositories.length?this._renderNoResultsFound():this._renderRepositories()}
        </div>
      </div>
      <ha-fab
        slot="fab"
        .label=${this.hacs.localize("store.add")}
        extended
        @click=${this._addRepository}
      >
        <ha-svg-icon slot="icon" .path=${P}></ha-svg-icon>
      </ha-fab>
    </hass-tabs-subpage>`}},{kind:"method",key:"_renderRepositories",value:function(){return this.visibleRepositories.map(t=>r`<hacs-repository-card
          .hass=${this.hass}
          .hacs=${this.hacs}
          .repository=${t}
          .narrow=${this.narrow}
          ?narrow=${this.narrow}
          .status=${this.hacs.status}
          .removed=${this.hacs.removed}
          .addedToLovelace=${this.hacs.addedToLovelace(this.hacs,t)}
        ></hacs-repository-card>`)}},{kind:"method",key:"_renderNoResultsFound",value:function(){return r`<ha-card class="no-repositories">
      <div class="header">${this.hacs.localize("store.no_repositories")} 😕</div>
      <p>
        ${this.hacs.localize("store.no_repositories_found_desc1").replace("{searchInput}",this._searchInput)}
        <br />
        ${this.hacs.localize("store.no_repositories_found_desc2")}
      </p>
    </ha-card>`}},{kind:"method",key:"_renderEmpty",value:function(){return r`<ha-card class="no-repositories">
      <div class="header">${this.hacs.localize("store.no_repositories")} 😕</div>
      <p>
        ${this.hacs.localize("store.no_repositories_desc1")}<br />${this.hacs.localize("store.no_repositories_desc2")}
      </p>
    </ha-card>`}},{kind:"method",key:"_inputValueChanged",value:function(t){this._searchInput=t.detail.value,window.localStorage.setItem("hacs-search",this._searchInput)}},{kind:"method",key:"_addRepository",value:function(){this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"add-repository",repositories:this.repositories,section:this.section},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[T,H,U,j,G,c`
        .filter {
          border-bottom: 1px solid var(--divider-color);
        }
        .content {
          height: calc(100vh - 128px);
          overflow: auto;
        }
        .narrow-content {
          height: calc(100vh - 128px);
        }
        .container {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
          justify-items: center;
          grid-gap: 8px 8px;
          padding: 8px 16px 16px;
          margin-bottom: 64px;
        }
        .no-repositories {
          width: 100%;
          text-align: center;
          margin-top: 12px;
        }
        .new-repositories {
          margin: 4px 16px 0 16px;
          color: var(--hcv-text-color-primary);
        }
        hacs-repository-card {
          max-width: 500px;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
        }
        hacs-repository-card[narrow] {
          width: 100%;
        }
        hacs-repository-card[narrow]:last-of-type {
          margin-bottom: 64px;
        }
        .narrow {
          width: 100%;
          display: block;
          padding: 0px;
          margin: 0;
        }

        .container .narrow {
          margin-bottom: 128px;
        }

        .bottom-bar {
          position: fixed !important;
        }
      `]}}]}}),a);export{Re as HacsStorePanel};
