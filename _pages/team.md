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
<div class="team-row team-row-pi">
  <div class="team-row-photo-wrap">
    {% if person.url %}<a href="{{ person.url }}" target="_blank">{% endif %}
    <img src="/assets/img/{{ person.photo }}" class="team-row-photo" alt="{{ person.name }}">
    {% if person.url %}</a>{% endif %}
  </div>
  <div class="team-row-info">
    <h3>{% if person.url %}<a href="{{ person.url }}" target="_blank">{{ person.name }}</a>{% else %}{{ person.name }}{% endif %}</h3>
    <p class="role">{{ person.role }}</p>
    {% if person.email or person.twitter or person.github %}
    <div class="team-social-links">
      {% if person.email %}<a href="mailto:{{ person.email }}" aria-label="Email {{ person.name }}"><i class="fa-solid fa-envelope"></i></a>{% endif %}
      {% if person.twitter %}<a href="{{ person.twitter }}" target="_blank" aria-label="{{ person.name }} on Twitter/X"><i class="fa-brands fa-x-twitter"></i></a>{% endif %}
      {% if person.github %}<a href="{{ person.github }}" target="_blank" aria-label="{{ person.name }} on GitHub"><i class="fa-brands fa-github"></i></a>{% endif %}
    </div>
    {% endif %}
    {% if person.bio %}<div class="team-row-bio"><p>{{ person.bio }}</p></div>{% endif %}
    {% if person.cheese %}<span class="cheese-tag">{{ person.cheese }}</span>{% endif %}
  </div>
</div>
{% endfor %}
</div>

## Postdoctoral Researchers

<div class="team-grid">
{% for person in site.data.team.postdocs %}
{% include team-card.liquid person=person %}
{% endfor %}
</div>

## PhD Students

<div class="team-grid">
{% for person in site.data.team.phd %}
{% include team-card.liquid person=person %}
{% endfor %}
</div>

## Masters Students

<div class="team-grid">
{% for person in site.data.team.masters %}
{% include team-card.liquid person=person %}
{% endfor %}
</div>

## Research Assistants

<div class="team-grid">
{% for person in site.data.team.ra %}
{% include team-card.liquid person=person %}
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
