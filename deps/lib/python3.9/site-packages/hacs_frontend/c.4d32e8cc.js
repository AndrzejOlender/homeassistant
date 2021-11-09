import{y as t,z as e,M as i,A as o,e as r,o as s,B as a,T as n,b as l,r as c,n as d,_ as h,H as p,J as m,m as f,S as g,O as y,U as u,V as v,W as b,X as _,Y as w}from"./main-60575625.js";import"./c.b82b3683.js";import"./c.5bd359ff.js";import"./c.75898fa6.js";import{F as k}from"./c.309b4815.js";import{o as x}from"./c.5325c693.js";import{o as $}from"./c.e32d17dc.js";import"./c.a1ea1e73.js";import{s as z}from"./c.6d478880.js";import{u as R}from"./c.997269e7.js";import"./c.659eb0c9.js";import"./c.0f3aa98b.js";import"./c.40bbc652.js";import"./c.386ba692.js";import"./c.d3dbc78b.js";var j={ROOT:"mdc-form-field"},E={LABEL_SELECTOR:".mdc-form-field > label"},I=function(i){function o(t){var r=i.call(this,e(e({},o.defaultAdapter),t))||this;return r.click=function(){r.handleClick()},r}return t(o,i),Object.defineProperty(o,"cssClasses",{get:function(){return j},enumerable:!1,configurable:!0}),Object.defineProperty(o,"strings",{get:function(){return E},enumerable:!1,configurable:!0}),Object.defineProperty(o,"defaultAdapter",{get:function(){return{activateInputRipple:function(){},deactivateInputRipple:function(){},deregisterInteractionHandler:function(){},registerInteractionHandler:function(){}}},enumerable:!1,configurable:!0}),o.prototype.init=function(){this.adapter.registerInteractionHandler("click",this.click)},o.prototype.destroy=function(){this.adapter.deregisterInteractionHandler("click",this.click)},o.prototype.handleClick=function(){var t=this;this.adapter.activateInputRipple(),requestAnimationFrame((function(){t.adapter.deactivateInputRipple()}))},o}(i);class B extends a{constructor(){super(...arguments),this.alignEnd=!1,this.spaceBetween=!1,this.nowrap=!1,this.label="",this.mdcFoundationClass=I}createAdapter(){return{registerInteractionHandler:(t,e)=>{this.labelEl.addEventListener(t,e)},deregisterInteractionHandler:(t,e)=>{this.labelEl.removeEventListener(t,e)},activateInputRipple:async()=>{const t=this.input;if(t instanceof k){const e=await t.ripple;e&&e.startPress()}},deactivateInputRipple:async()=>{const t=this.input;if(t instanceof k){const e=await t.ripple;e&&e.endPress()}}}}get input(){var t,e;return null!==(e=null===(t=this.slottedInputs)||void 0===t?void 0:t[0])&&void 0!==e?e:null}render(){const t={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return n`
      <div class="mdc-form-field ${l(t)}">
        <slot></slot>
        <label class="mdc-label"
               @click="${this._labelClick}">${this.label}</label>
      </div>`}_labelClick(){const t=this.input;t&&(t.focus(),t.click())}}o([r({type:Boolean})],B.prototype,"alignEnd",void 0),o([r({type:Boolean})],B.prototype,"spaceBetween",void 0),o([r({type:Boolean})],B.prototype,"nowrap",void 0),o([r({type:String}),x((async function(t){const e=this.input;e&&("input"===e.localName?e.setAttribute("aria-label",t):e instanceof k&&(await e.updateComplete,e.setAriaLabel(t)))}))],B.prototype,"label",void 0),o([s(".mdc-form-field")],B.prototype,"mdcRoot",void 0),o([$("",!0,"*")],B.prototype,"slottedInputs",void 0),o([s("label")],B.prototype,"labelEl",void 0);const C=c`.mdc-form-field{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));display:inline-flex;align-items:center;vertical-align:middle}.mdc-form-field>label{margin-left:0;margin-right:auto;padding-left:4px;padding-right:0;order:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{margin-left:auto;margin-right:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{padding-left:0;padding-right:4px}.mdc-form-field--nowrap>label{text-overflow:ellipsis;overflow:hidden;white-space:nowrap}.mdc-form-field--align-end>label{margin-left:auto;margin-right:0;padding-left:0;padding-right:4px;order:-1}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{margin-left:0;margin-right:auto}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{padding-left:4px;padding-right:0}.mdc-form-field--space-between{justify-content:space-between}.mdc-form-field--space-between>label{margin:0}[dir=rtl] .mdc-form-field--space-between>label,.mdc-form-field--space-between>label[dir=rtl]{margin:0}:host{display:inline-flex}.mdc-form-field{width:100%}::slotted(*){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}::slotted(mwc-switch){margin-right:10px}[dir=rtl] ::slotted(mwc-switch),::slotted(mwc-switch[dir=rtl]){margin-left:10px}`;let A=class extends B{};A.styles=[C],A=o([d("mwc-formfield")],A),h([d("ha-formfield")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"get",static:!0,key:"styles",value:function(){return[A.styles,c`
        :host(:not([alignEnd])) ::slotted(ha-switch) {
          margin-right: 10px;
        }
        :host([dir="rtl"]:not([alignEnd])) ::slotted(ha-switch) {
          margin-left: 10px;
          margin-right: auto;
        }
      `]}}]}}),A);let H=h([d("hacs-install-dialog")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[r()],key:"repository",value:void 0},{kind:"field",decorators:[r()],key:"_repository",value:void 0},{kind:"field",decorators:[r()],key:"_toggle",value:()=>!0},{kind:"field",decorators:[r()],key:"_installing",value:()=>!1},{kind:"field",decorators:[r()],key:"_error",value:void 0},{kind:"field",decorators:[m()],key:"_version",value:void 0},{kind:"method",key:"shouldUpdate",value:function(t){return t.forEach((t,e)=>{"hass"===e&&(this.sidebarDocked='"docked"'===window.localStorage.getItem("dockedSidebar")),"repositories"===e&&(this._repository=this._getRepository(this.repositories,this.repository))}),t.has("sidebarDocked")||t.has("narrow")||t.has("active")||t.has("_toggle")||t.has("_error")||t.has("_version")||t.has("_repository")||t.has("_installing")}},{kind:"field",key:"_getRepository",value:()=>f((t,e)=>null==t?void 0:t.find(t=>t.id===e))},{kind:"field",key:"_getInstallPath",value:()=>f(t=>{let e=t.local_path;return"theme"===t.category&&(e=`${e}/${t.file_name}`),e})},{kind:"method",key:"firstUpdated",value:async function(){this._repository=this._getRepository(this.repositories,this.repository),this._repository.updated_info||(await g(this.hass,this._repository.id),this.repositories=await y(this.hass)),this._toggle=!1,this.hass.connection.subscribeEvents(t=>this._error=t.data,"hacs/error")}},{kind:"method",key:"render",value:function(){if(!this.active||!this._repository)return n``;const t=this._getInstallPath(this._repository);return n`
      <hacs-dialog
        .active=${this.active}
        .narrow=${this.narrow}
        .hass=${this.hass}
        .secondary=${this.secondary}
        .title=${this._repository.name}
        dynamicHeight
      >
        <div class="content">
          ${"version"===this._repository.version_or_commit?n`<div class="beta-container">
                  <ha-formfield .label=${this.hacs.localize("dialog_install.show_beta")}>
                    <ha-switch
                      ?disabled=${this._toggle}
                      .checked=${this._repository.beta}
                      @change=${this._toggleBeta}
                    ></ha-switch>
                  </ha-formfield>
                </div>
                <div class="version-select-container">
                  <ha-paper-dropdown-menu
                    ?disabled=${this._toggle}
                    class="version-select-dropdown"
                    label="${this.hacs.localize("dialog_install.select_version")}"
                  >
                    <paper-listbox
                      id="version"
                      class="version-select-list"
                      slot="dropdown-content"
                      selected="0"
                      @iron-select=${this._versionSelectChanged}
                    >
                      ${this._repository.releases.map(t=>n`<paper-item .version=${t} class="version-select-item"
                            >${t}</paper-item
                          >`)}
                      ${"hacs/integration"===this._repository.full_name||this._repository.hide_default_branch?"":n`
                            <paper-item
                              .version=${this._repository.default_branch}
                              class="version-select-item"
                              >${this._repository.default_branch}</paper-item
                            >
                          `}
                    </paper-listbox>
                  </ha-paper-dropdown-menu>
                </div>`:""}
          ${this._repository.can_install?"":n`<p class="error">
                ${this.hacs.localize("confirm.home_assistant_version_not_correct").replace("{haversion}",this.hass.config.version).replace("{minversion}",this._repository.homeassistant)}
              </p>`}
          <div class="note">
            ${this.hacs.localize("repository.note_installed")}
            <code>'${t}'</code>
            ${"plugin"===this._repository.category&&"storage"!==this.hacs.status.lovelace_mode?n`
                  <p>${this.hacs.localize("repository.lovelace_instruction")}</p>
                  <pre>
                url: ${u({repository:this._repository,skipTag:!0})}
                type: module
                </pre
                  >
                `:""}
            ${"integration"===this._repository.category?n`<p>${this.hacs.localize("dialog_install.restart")}</p>`:""}
          </div>
          ${this._error?n`<div class="error">${this._error.message}</div>`:""}
        </div>
        <mwc-button
          slot="primaryaction"
          ?disabled=${!this._repository.can_install||this._toggle}
          @click=${this._installRepository}
          >${this._installing?n`<ha-circular-progress active size="small"></ha-circular-progress>`:this.hacs.localize("common.install")}</mwc-button
        >
        <hacs-link slot="secondaryaction" .url="https://github.com/${this._repository.full_name}"
          ><mwc-button>${this.hacs.localize("common.repository")}</mwc-button></hacs-link
        >
      </hacs-dialog>
    `}},{kind:"method",key:"_versionSelectChanged",value:function(t){t.currentTarget.selectedItem.version!==this._version&&(this._version=t.currentTarget.selectedItem.version)}},{kind:"method",key:"_toggleBeta",value:async function(){this._toggle=!0,await v(this.hass,this.repository),this.repositories=await y(this.hass),this._toggle=!1}},{kind:"method",key:"_installRepository",value:async function(){var t;if(this._installing=!0,this._repository){if("commit"!==(null===(t=this._repository)||void 0===t?void 0:t.version_or_commit)){const t=this._version||this._repository.available_version||this._repository.default_branch;await b(this.hass,this._repository.id,t)}else await _(this.hass,this._repository.id);this.hacs.log.debug(this._repository.category,"_installRepository"),this.hacs.log.debug(this.hacs.status.lovelace_mode,"_installRepository"),"plugin"===this._repository.category&&"storage"===this.hacs.status.lovelace_mode&&await R(this.hass,this._repository,this._version),this._installing=!1,this.dispatchEvent(new Event("hacs-secondary-dialog-closed",{bubbles:!0,composed:!0})),this.dispatchEvent(new Event("hacs-dialog-closed",{bubbles:!0,composed:!0})),"plugin"===this._repository.category&&"storage"===this.hacs.status.lovelace_mode&&z(this,{title:this.hacs.localize("common.reload"),text:n`${this.hacs.localize("dialog.reload.description")}</br>${this.hacs.localize("dialog.reload.confirm")}`,dismissText:this.hacs.localize("common.cancel"),confirmText:this.hacs.localize("common.reload"),confirm:()=>{w.location.href=w.location.href}})}}},{kind:"get",static:!0,key:"styles",value:function(){return[c`
        .version-select-dropdown {
          width: 100%;
        }
        .content {
          padding: 32px 8px;
        }
        .note {
          margin-bottom: -32px;
          margin-top: 12px;
        }
        .lovelace {
          margin-top: 8px;
        }
        .error {
          color: var(--hacs-error-color, var(--google-red-500));
        }
        paper-menu-button {
          color: var(--secondary-text-color);
          padding: 0;
        }
        paper-item {
          cursor: pointer;
        }
        paper-item-body {
          opacity: var(--dark-primary-opacity);
        }
        pre {
          white-space: pre-line;
          user-select: all;
        }
      `]}}]}}),p);export{H as HacsInstallDialog};
