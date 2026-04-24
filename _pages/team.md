---
layout: page
permalink: /team/
title: Team
description:
nav: true
nav_order: 3
---

## Principal Investigator

<div class="team-rows-group">
{% for person in site.data.team.pi %}
{% if person.bio %}
<details class="team-row">
  <summary>
    <div class="team-row-photo-wrap">
      {% if person.url %}<a href="{{ person.url }}" target="_blank">{% endif %}
      <img src="/assets/img/{{ person.photo }}" class="team-row-photo" alt="{{ person.name }}">
      {% if person.url %}</a>{% endif %}
    </div>
    <div class="team-row-info">
      <h3>{% if person.url %}<a href="{{ person.url }}" target="_blank">{{ person.name }}</a>{% else %}{{ person.name }}{% endif %}</h3>
      <p class="role">{{ person.role }}</p>
      {% if person.cheese %}<span class="cheese-tag">{{ person.cheese }}</span>{% endif %}
    </div>
    <span class="team-row-chevron">▶</span>
  </summary>
  <div class="team-row-bio"><p>{{ person.bio }}</p></div>
</details>
{% else %}
<div class="team-row">
  <div class="team-row-photo-wrap">
    {% if person.url %}<a href="{{ person.url }}" target="_blank">{% endif %}
    <img src="/assets/img/{{ person.photo }}" class="team-row-photo" alt="{{ person.name }}">
    {% if person.url %}</a>{% endif %}
  </div>
  <div class="team-row-info">
    <h3>{% if person.url %}<a href="{{ person.url }}" target="_blank">{{ person.name }}</a>{% else %}{{ person.name }}{% endif %}</h3>
    <p class="role">{{ person.role }}</p>
    {% if person.cheese %}<span class="cheese-tag">{{ person.cheese }}</span>{% endif %}
  </div>
</div>
{% endif %}
{% endfor %}
</div>

## Postdoctoral Researchers

<div class="team-rows-group">
{% for person in site.data.team.postdocs %}
{% if person.bio %}
<details class="team-row">
  <summary>
    <div class="team-row-photo-wrap">
      {% if person.url %}<a href="{{ person.url }}" target="_blank">{% endif %}
      <img src="/assets/img/{{ person.photo }}" class="team-row-photo" alt="{{ person.name }}">
      {% if person.url %}</a>{% endif %}
    </div>
    <div class="team-row-info">
      <h3>{% if person.url %}<a href="{{ person.url }}" target="_blank">{{ person.name }}</a>{% else %}{{ person.name }}{% endif %}</h3>
      <p class="role">{{ person.role }}</p>
      {% if person.cheese %}<span class="cheese-tag">{{ person.cheese }}</span>{% endif %}
    </div>
    <span class="team-row-chevron">▶</span>
  </summary>
  <div class="team-row-bio"><p>{{ person.bio }}</p></div>
</details>
{% else %}
<div class="team-row">
  <div class="team-row-photo-wrap">
    {% if person.url %}<a href="{{ person.url }}" target="_blank">{% endif %}
    <img src="/assets/img/{{ person.photo }}" class="team-row-photo" alt="{{ person.name }}">
    {% if person.url %}</a>{% endif %}
  </div>
  <div class="team-row-info">
    <h3>{% if person.url %}<a href="{{ person.url }}" target="_blank">{{ person.name }}</a>{% else %}{{ person.name }}{% endif %}</h3>
    <p class="role">{{ person.role }}</p>
    {% if person.cheese %}<span class="cheese-tag">{{ person.cheese }}</span>{% endif %}
  </div>
</div>
{% endif %}
{% endfor %}
</div>

## PhD Students

<div class="team-rows-group">
{% for person in site.data.team.phd %}
{% if person.bio %}
<details class="team-row">
  <summary>
    <div class="team-row-photo-wrap">
      {% if person.url %}<a href="{{ person.url }}" target="_blank">{% endif %}
      <img src="/assets/img/{{ person.photo }}" class="team-row-photo" alt="{{ person.name }}">
      {% if person.url %}</a>{% endif %}
    </div>
    <div class="team-row-info">
      <h3>{% if person.url %}<a href="{{ person.url }}" target="_blank">{{ person.name }}</a>{% else %}{{ person.name }}{% endif %}</h3>
      <p class="role">{{ person.role }}</p>
      {% if person.cheese %}<span class="cheese-tag">{{ person.cheese }}</span>{% endif %}
    </div>
    <span class="team-row-chevron">▶</span>
  </summary>
  <div class="team-row-bio"><p>{{ person.bio }}</p></div>
</details>
{% else %}
<div class="team-row">
  <div class="team-row-photo-wrap">
    {% if person.url %}<a href="{{ person.url }}" target="_blank">{% endif %}
    <img src="/assets/img/{{ person.photo }}" class="team-row-photo" alt="{{ person.name }}">
    {% if person.url %}</a>{% endif %}
  </div>
  <div class="team-row-info">
    <h3>{% if person.url %}<a href="{{ person.url }}" target="_blank">{{ person.name }}</a>{% else %}{{ person.name }}{% endif %}</h3>
    <p class="role">{{ person.role }}</p>
    {% if person.cheese %}<span class="cheese-tag">{{ person.cheese }}</span>{% endif %}
  </div>
</div>
{% endif %}
{% endfor %}
</div>

## Masters Students

<div class="team-rows-group">
{% for person in site.data.team.masters %}
{% if person.bio %}
<details class="team-row">
  <summary>
    <div class="team-row-photo-wrap">
      {% if person.url %}<a href="{{ person.url }}" target="_blank">{% endif %}
      <img src="/assets/img/{{ person.photo }}" class="team-row-photo" alt="{{ person.name }}">
      {% if person.url %}</a>{% endif %}
    </div>
    <div class="team-row-info">
      <h3>{% if person.url %}<a href="{{ person.url }}" target="_blank">{{ person.name }}</a>{% else %}{{ person.name }}{% endif %}</h3>
      <p class="role">{{ person.role }}</p>
      {% if person.cheese %}<span class="cheese-tag">{{ person.cheese }}</span>{% endif %}
    </div>
    <span class="team-row-chevron">▶</span>
  </summary>
  <div class="team-row-bio"><p>{{ person.bio }}</p></div>
</details>
{% else %}
<div class="team-row">
  <div class="team-row-photo-wrap">
    {% if person.url %}<a href="{{ person.url }}" target="_blank">{% endif %}
    <img src="/assets/img/{{ person.photo }}" class="team-row-photo" alt="{{ person.name }}">
    {% if person.url %}</a>{% endif %}
  </div>
  <div class="team-row-info">
    <h3>{% if person.url %}<a href="{{ person.url }}" target="_blank">{{ person.name }}</a>{% else %}{{ person.name }}{% endif %}</h3>
    <p class="role">{{ person.role }}</p>
    {% if person.cheese %}<span class="cheese-tag">{{ person.cheese }}</span>{% endif %}
  </div>
</div>
{% endif %}
{% endfor %}
</div>

## Research Assistants

<div class="team-rows-group">
{% for person in site.data.team.ra %}
{% if person.bio %}
<details class="team-row">
  <summary>
    <div class="team-row-photo-wrap">
      {% if person.url %}<a href="{{ person.url }}" target="_blank">{% endif %}
      <img src="/assets/img/{{ person.photo }}" class="team-row-photo" alt="{{ person.name }}">
      {% if person.url %}</a>{% endif %}
    </div>
    <div class="team-row-info">
      <h3>{% if person.url %}<a href="{{ person.url }}" target="_blank">{{ person.name }}</a>{% else %}{{ person.name }}{% endif %}</h3>
      <p class="role">{{ person.role }}</p>
      {% if person.cheese %}<span class="cheese-tag">{{ person.cheese }}</span>{% endif %}
    </div>
    <span class="team-row-chevron">▶</span>
  </summary>
  <div class="team-row-bio"><p>{{ person.bio }}</p></div>
</details>
{% else %}
<div class="team-row">
  <div class="team-row-photo-wrap">
    {% if person.url %}<a href="{{ person.url }}" target="_blank">{% endif %}
    <img src="/assets/img/{{ person.photo }}" class="team-row-photo" alt="{{ person.name }}">
    {% if person.url %}</a>{% endif %}
  </div>
  <div class="team-row-info">
    <h3>{% if person.url %}<a href="{{ person.url }}" target="_blank">{{ person.name }}</a>{% else %}{{ person.name }}{% endif %}</h3>
    <p class="role">{{ person.role }}</p>
    {% if person.cheese %}<span class="cheese-tag">{{ person.cheese }}</span>{% endif %}
  </div>
</div>
{% endif %}
{% endfor %}
</div>

## Alumni

<ul>
{% for person in site.data.team.alumni %}
  <li>{{ person.name }}{% if person.role %}, {{ person.role }}{% endif %}</li>
{% endfor %}
</ul>

<div class="lab-life-link-wrap">
  <a href="/photos/" class="lab-life-link">Life outside the lab</a>
</div>
