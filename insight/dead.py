# Dead CODE FROM INSIGHT


# ----------------------------
# insight/insight.py

# # Add one insight
# class InsightCreate(CreateView):
#     model = Insight
#     template_name = 'insight_add.html'
#     fields = ['name', 'topic']
#
# # Delete a insight
# class InsightDelete(DeleteView):
#     model = Insight
#     template_name = 'insight_delete.html'
#     success_url = reverse_lazy('insight-list')


# ----------------------------
# templates/insight_add.html
#
# {% extends "insight_theme.html" %}
#
#
# {% block content %}
#
# <h3>Add Insight</h3>
#
#
# <form action="" method="post">{% csrf_token %}
#     {{ form.as_p }}
#     <input type="submit" value="Save Note" class="button" />
#     <a href=".." class="button">Cancel</a>
#
# </form>
#
#
# {% endblock %}


# ----------------------------
# templates/insight_delete.html

# {% extends "insight.html" %}
#
# {% block content %}
#
# <h3>Delete Note</h3>
#
# <form action="" method="post">
#     {% csrf_token %}
#
#     <p>
#         This object as well as their related objects will be deleted.
#         Are you sure?
#     </p>
#
#     <p>
#         <a href="{{ object.get_absolute_url }}">Note #{{ object.pk}} - {{ object.title }}</a>
#     </p>
#
#     <input type="submit" value="Confirm" name="confirm_delete" class="button" />
#     <a href="../.." class="button">Cancel</a>
#     <input type="hidden" value="{{ object.id }}" name="itemsToDelete" />
# </form>
#
#
# {% endblock %}
