import{_ as i,H as s,e as t,m as o,Y as e,Q as a,y as r,aj as c,ak as h,al as n,am as l,an as d,c as p,r as u,n as y}from"./main-add588c4.js";import{m}from"./c.ca19eb00.js";import"./c.25460dea.js";import"./c.c3a2aae1.js";import"./c.eb1f5cc8.js";import"./c.a8d8c686.js";import"./c.9f27b448.js";import"./c.0a038163.js";let _=i([y("hacs-repository-info-dialog")],(function(i,s){return{F:class extends s{constructor(...s){super(...s),i(this)}},d:[{kind:"field",decorators:[t()],key:"repository",value:void 0},{kind:"field",decorators:[t()],key:"_repository",value:void 0},{kind:"field",key:"_getRepository",value:()=>o((i,s)=>null==i?void 0:i.find(i=>i.id===s))},{kind:"field",key:"_getAuthors",value:()=>o(i=>{const s=[];if(!i.authors)return s;if(i.authors.forEach(i=>s.push(i.replace("@",""))),0===s.length){const t=i.full_name.split("/")[0];if(["custom-cards","custom-components","home-assistant-community-themes"].includes(t))return s;s.push(t)}return s})},{kind:"method",key:"shouldUpdate",value:function(i){return i.forEach((i,s)=>{"hass"===s&&(this.sidebarDocked='"docked"'===window.localStorage.getItem("dockedSidebar")),"repositories"===s&&(this._repository=this._getRepository(this.repositories,this.repository))}),i.has("sidebarDocked")||i.has("narrow")||i.has("active")||i.has("_repository")}},{kind:"method",key:"firstUpdated",value:async function(){this._repository=this._getRepository(this.repositories,this.repository),this._repository.updated_info||(await e(this.hass,this._repository.id),this.repositories=await a(this.hass))}},{kind:"method",key:"render",value:function(){if(!this.active)return r``;const i=this._getAuthors(this._repository);return r`
      <hacs-dialog
        .noActions=${this._repository.installed}
        .active=${this.active}
        .title=${this._repository.name||""}
        .hass=${this.hass}
        ><div class="content scroll">
          ${this._repository.updated_info?r`
            <div class="chips">
              ${this._repository.installed?r`<hacs-chip
                    title="${this.hacs.localize("dialog_info.version_installed")}"
                    .icon=${c}
                    .value=${this._repository.installed_version}
                  ></hacs-chip>`:""}
              ${i?i.map(i=>r`<hacs-chip
                      title="${this.hacs.localize("dialog_info.author")}"
                      .url="https://github.com/${i}"
                      .icon=${h}
                      .value="@${i}"
                    ></hacs-chip>`):""}
              ${this._repository.downloads?r` <hacs-chip
                    title="${this.hacs.localize("dialog_info.downloads")}"
                    .icon=${n}
                    .value=${this._repository.downloads}
                  ></hacs-chip>`:""}
              <hacs-chip
                title="${this.hacs.localize("dialog_info.stars")}"
                .icon=${l}
                .value=${this._repository.stars}
              ></hacs-chip>
              <hacs-chip
                title="${this.hacs.localize("dialog_info.open_issues")}"
                .icon=${d}
                .value=${this._repository.issues}
                .url="https://github.com/${this._repository.full_name}/issues"
              ></hacs-chip>
            </div>
            ${m.html(this._repository.additional_info||this.hacs.localize("dialog_info.no_info"),this._repository)}`:r`
            <div class="loading">
              <ha-circular-progress active size="large"></ha-circular-progress>
            </div>
          `}
        </div>
        ${!this._repository.installed&&this._repository.updated_info?r`
              <mwc-button slot="primaryaction" @click=${this._installRepository}
                >${this.hacs.localize("dialog_info.install")}</mwc-button
              ><hacs-link
                slot="secondaryaction"
                .url="https://github.com/${this._repository.full_name}"
                ><mwc-button>${this.hacs.localize("dialog_info.open_repo")}</mwc-button></hacs-link
              >
            `:""}
      </hacs-dialog>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[p,u`
        .content {
          width: 100%;
          overflow: auto;
        }
        img {
          max-width: 100%;
        }
        .loading {
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 4rem 8rem;
        }
        .chips {
          display: flex;
          padding-bottom: 8px;
        }
        hacs-chip {
          margin: 0 4px;
        }
        div.chips hacs-link {
          margin: -24px 4px;
        }
        hacs-link mwc-button {
          margin-top: -18px;
        }
      `]}},{kind:"method",key:"_installRepository",value:async function(){this.dispatchEvent(new CustomEvent("hacs-dialog-secondary",{detail:{type:"install",repository:this._repository.id},bubbles:!0,composed:!0}))}}]}}),s);export{_ as HacsRepositoryDialog};
